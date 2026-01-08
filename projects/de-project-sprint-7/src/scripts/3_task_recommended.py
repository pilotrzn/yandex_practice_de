import sys
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.window import Window
import pyspark.sql.functions as F


def createSpark(date: str) -> SparkSession:
    conf = SparkConf() \
        .setAppName(f"Project_RecommendMart-{date}") \
        .set("spark.sql.shuffle.partitions", "200") \
        .set("spark.executor.memoryOverhead", "2G")
    sc = SparkContext(conf=conf)
    return SQLContext(sc)


def main():
    date = sys.argv[1]
    base_input_path = sys.argv[2]
    city_geo_path = sys.argv[3]
    actual_cities_path = sys.argv[4]
    base_output_path = sys.argv[5]

    spark = createSpark(date)

    # 1. Загрузка данных о городах
    geo_df = spark.read.options(delimiter=';', header=True).csv(city_geo_path) \
        .select(
            F.col('id').alias('zone_id'),
            F.col('city'),
            F.regexp_replace('lat', ',', '.').cast('double').alias('lat'),
            F.regexp_replace('lng', ',', '.').cast('double').alias('lng'),
            'timezone'
        )

    # 2. Загрузка и подготовка событий
    events = spark.read.parquet(f'{base_input_path}') \
        .filter(F.col("date") == F.lit(date)) \
        .select(
            F.col('event.message_from'),
            F.col('event.user'),
            F.col('event.message_to'),
            F.col('lat'),
            F.col('lon').alias('lng'),
            F.coalesce('event.message_ts', 'event.datetime').alias('event_time'),
            F.col('event_type'),
            F.col('event.subscription_channel')
        )

    # 3. Разделяем события на сообщения и подписки
    messages = events.filter(F.col("event_type") == "message")
    subscriptions = events.filter(F.col("event_type") == "subscription")

    # 4. Получаем последние локации пользователей (только из сообщений)
    window_msg = Window.partitionBy("message_from").orderBy(F.col("event_time").asc())
    user_last_location = messages \
        .withColumn('rank', F.row_number().over(window_msg)) \
        .filter(F.col("rank") == 1) \
        .select(
            F.col('message_from').alias('user_id'),
            'lat',
            'lng'
        )

    # 5. Получаем все направленные контакты (только из сообщений)
    directed_contacts = messages \
        .filter(F.col("message_to").isNotNull()) \
        .select(
            F.col("message_from").alias("sender_id"),
            F.col("message_to").alias("receiver_id")
        ).distinct()

    # 6. Получаем факт любого взаимодействия между пользователями
    any_contact = directed_contacts.select(
        F.least("sender_id", "receiver_id").alias("user1"),
        F.greatest("sender_id", "receiver_id").alias("user2")
    ).distinct()

    # 7. Получаем подписки пользователей
    user_subscriptions = subscriptions \
        .filter(F.col("subscription_channel").isNotNull()) \
        .select(
            F.col("user").alias("user_id"),
            F.col("subscription_channel").alias("channel")
        )

    # 8. Генерируем пары с общими подписками
    common_subs = user_subscriptions.alias("s1") \
        .join(user_subscriptions.alias("s2"),
            (F.col("s1.channel") == F.col("s2.channel")) & 
            (F.col("s1.user_id") < F.col("s2.user_id"))) \
        .select(
            F.col("s1.user_id").alias("user_left"),
            F.col("s2.user_id").alias("user_right")
        )

    # 9. Исключаем пары, которые уже имели любые контакты
    potential_pairs = common_subs.join(
        any_contact,
        ((F.col("user_left") == F.col("user1")) & 
         (F.col("user_right") == F.col("user2"))),
        "left_anti"
    )

    # 10. Получаем актуальные города пользователей
    actual_cities = spark.read.parquet(f'{actual_cities_path}/date={date}') \
        .join(geo_df, F.col("act_city") == F.col("city"), 'left') \
        .select(
            F.col('user_id').cast('string'), 
            F.col('zone_id'), 
            F.col('timezone'),
            F.col('local_time')
        )

    # 11. Фильтруем по расстоянию и добавляем zone_id
    result = potential_pairs \
        .join(user_last_location.alias("ul"),
            F.col("user_left") == F.col("ul.user_id")) \
        .join(user_last_location.alias("ur"),
            F.col("user_right") == F.col("ur.user_id")) \
        .withColumn("distance_km", 
            F.acos(
                F.sin(F.radians("ul.lat")) * F.sin(F.radians("ur.lat")) +
                F.cos(F.radians("ul.lat")) * F.cos(F.radians("ur.lat")) * 
                F.cos(F.radians("ul.lng") - F.radians("ur.lng"))
            ) * F.lit(6371)) \
        .filter(F.col("distance_km") <= 1) \
        .join(actual_cities.alias("ac"),
            F.col("user_left") == F.col("ac.user_id")) \
        .withColumn("processed_dttm", F.current_timestamp()) \
        .select(
            "user_left",
            "user_right",
            "processed_dttm",
            "ac.zone_id",
            "ac.local_time"
        )

    # 12. Сохраняем результат
    result.repartition(1) \
        .write \
        .format('parquet') \
        .mode("overwrite") \
        .save(f"{base_output_path}/date={date}")

if __name__ == "__main__":
    main()