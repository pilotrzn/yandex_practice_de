import sys
import math
from pyspark.sql import SparkSession, DataFrame
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import DoubleType
from pyspark.sql.window import Window
import pyspark.sql.functions as F


def createSpark(date: str) -> SparkSession:
    conf = SparkConf() \
        .setAppName(f"Project_User_Geo-{date}") \
        .set("spark.sql.shuffle.partitions", "200") \
        .set("spark.executor.memoryOverhead", "2G")

    sc = SparkContext(conf=conf)
    return SQLContext(sc)


def calculate_distance(lat1, lon1, lat2, lon2):
    # Конвертация градусов в радианы
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    # Разницы координат
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    # Формула гаверсинусов
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    result = 6371 * (2 * math.asin(math.sqrt(a)))
    # Радиус Земли в километрах
    return result
# Регистрируем UDF функцию
calculate_distance_udf = F.udf(calculate_distance, DoubleType())


def add_travel_info(events_with_nearest_city) -> DataFrame:
    window_user_by_date = Window.partitionBy("user_id").orderBy("msg_date")
    # Добавляем порядковый номер сообщения для каждого пользователя
    df_with_sequence = events_with_nearest_city\
        .withColumn("msg_seq", F.row_number().over(window_user_by_date))
    # Шаг 2: Удаляем подряд идущие дубликаты городов
    # Добавляем флаг смены города
    df_with_city_changes = df_with_sequence\
        .withColumn("prev_city",F.lag("city").over(window_user_by_date))\
        .withColumn("city_changed",(F.col("city") != F.col("prev_city")) | F.col("prev_city").isNull())
    # Фильтруем только сообщения со сменой города
    df_city_changes_only = df_with_city_changes\
        .filter("city_changed")
    # Шаг 3: Собираем итоговую информацию о путешествиях
    df_travel_info = df_city_changes_only\
        .groupBy("user_id").agg(F.count("city").alias("travel_count"),
                                F.collect_list("city").alias("travel_array"))
    return df_travel_info


def add_home_city(events_with_nearest_city) -> DataFrame:
    # Шаг 1: Для каждого пользователя находим город с самой длинной непрерывной активностью
    window_user_city_date = Window.partitionBy("user_id", "city").orderBy("msg_date")
    # Добавляем флаг начала нового периода (если разница с предыдущей датой >1 день)
    df_with_periods = events_with_nearest_city \
        .withColumn("days_diff",
                    F.datediff("msg_date", F.lag("msg_date").over(window_user_city_date))) \
        .withColumn("new_period", (F.col("days_diff") > 1).cast("int"))
    # Создаем идентификаторы периодов непрерывной активности
    df_with_period_ids = df_with_periods\
        .withColumn("period_id", F.sum("new_period").over(window_user_city_date))
    # Группируем по периодам
    df_periods = df_with_period_ids\
        .groupBy("user_id", "city", "period_id")\
        .agg(
            F.min("msg_date").alias("period_start"),
            F.max("msg_date").alias("period_end"),
            F.count("*").alias("days_in_period"))
    # Находим самый длинный период для каждого пользователя
    window_user = Window.partitionBy("user_id").orderBy(
        F.desc("days_in_period"),
        F.desc("period_end")
    )
    df_longest_period = df_periods\
        .withColumn("rn", F.row_number().over(window_user))\
        .filter("rn = 1")\
        .select(
            "user_id",
            F.col("city").alias("home_city_candidate"),
            F.col("days_in_period"))
    # Шаг 2: Для пользователей без периода 27+ дней находим город с макс. сообщениями
    df_city_counts = events_with_nearest_city\
        .groupBy("user_id", "city")\
        .agg(
            F.count("*").alias("message_count"),
            F.min("msg_date").alias("first_msg_date"))

    window_user_count = Window.partitionBy("user_id").orderBy(
        F.desc("message_count"),
        F.asc("first_msg_date")  # при равенстве берем город первого сообщения
    )
    df_most_active_city = df_city_counts\
        .withColumn("rn", F.row_number().over(window_user_count))\
        .filter("rn = 1")\
        .select("user_id", F.col("city").alias("most_active_city"))
    # Шаг 3: Объединяем результаты
    df_home_city = df_longest_period.join(
        df_most_active_city, "user_id", "left")\
            .withColumn(
                "home_city",
                F.when(F.col("days_in_period") >= 27, F.col("home_city_candidate"))
                .otherwise(F.col("most_active_city")))\
            .select("user_id", "home_city")
    return df_home_city


def add_local_time_to_mart(events_with_cities_df):
    window_spec = Window.partitionBy("user_id").orderBy(F.col("msg_time").desc())

    last_events_df = events_with_cities_df \
        .withColumn("row_num", F.row_number().over(window_spec)) \
        .filter(F.col("row_num") == 1) \
        .select("user_id", "msg_time", "timezone")

    last_events_local_df = last_events_df.withColumn(
        "local_time",
        F.from_utc_timestamp(F.col("msg_time"), F.col("timezone")))
    return last_events_local_df


def main():
    date = sys.argv[1]
    base_input_path = sys.argv[2]
    city_geo_path = sys.argv[3]
    base_output_path = sys.argv[4]

    spark = createSpark(date)

    # Geta datas
    messages = spark.read.parquet(f'{base_input_path}')\
        .filter(
            (F.col("date") <= F.lit(date)) &
            (F.col("event_type") == 'message')) \
        .withColumn('msg_time', F.coalesce('event.message_ts', 'event.datetime'))\
        .select(
            F.col("event.message_id").alias("message_id"),
            F.col("event.message_from").alias("user_id"),
            F.col("lat").alias("msg_lat"),
            F.col("lon").alias("msg_lng"),
            F.col("date").alias("msg_date"),
            F.col("msg_time"))

    geo = spark.read.options(delimiter=';', header=True).csv(city_geo_path)
    geo = geo.withColumn(
        "geo_lat", F.regexp_replace(F.col("lat"), ",", ".").cast("double")) \
        .withColumn(
        "geo_lng", F.regexp_replace(F.col("lng"), ",", ".").cast("double"))

    events_with_cities = messages.crossJoin(geo)

    # расчет расстояний
    events_with_distances = events_with_cities.withColumn(
        "distance",
        calculate_distance_udf(
            F.col("msg_lat"),
            F.col("msg_lng"),
            F.col("geo_lat"),
            F.col("geo_lng")))

    window = Window().partitionBy(F.col("message_id")).orderBy(F.col("distance").asc())
    # события из ближайшего города
    events_with_nearest_city = events_with_distances \
        .withColumn("rank", F.row_number().over(window)) \
        .select(
            F.col("message_id"),
            F.col("user_id"),
            F.col("id").alias("zone_id"),
            F.col("city"),
            F.col("timezone"),
            F.col("msg_time"),
            F.col("msg_date"),
            F.col("rank")) \
        .filter(F.col("rank") == 1)
    
    window_auc = Window.partitionBy("user_id").orderBy(F.col("msg_time").desc())
    act_user_city = events_with_nearest_city \
        .withColumn("rank", F.row_number().over(window_auc)) \
        .filter(F.col("rank") == 1) \
        .select(F.col("user_id"), F.col("city").alias("act_city"))

    cities_list = act_user_city.join(
    events_with_nearest_city \
        .select(F.col('user_id'), F.col('msg_date'), F.col('city')) \
        .distinct() \
        .orderBy(F.col("user_id"), F.col("msg_date").desc()) \
        .groupBy("user_id") \
        .agg(F.collect_list("city")),
        'user_id', 'outer')

    df_home_city = add_home_city(events_with_nearest_city)
    df_travel_info = add_travel_info(events_with_nearest_city)
    df_local_times = add_local_time_to_mart(events_with_nearest_city)

    result = cities_list\
        .join(df_home_city, "user_id", "left") \
        .join(df_travel_info, "user_id", "left")\
        .join(df_local_times, "user_id", "left") \
        .select("user_id", "act_city", "home_city", "travel_count", "travel_array", "local_time")

    result.repartition(1) \
        .write \
        .format('parquet') \
        .mode("overwrite") \
        .save(f"{base_output_path}/date={date}")


if __name__ == "__main__":
    main()
