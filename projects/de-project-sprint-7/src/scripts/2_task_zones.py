import sys
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.window import Window
import pyspark.sql.functions as F


def createSpark(date: str) -> SparkSession:
    conf = SparkConf() \
        .setAppName(f"Project_ZonesMart-{date}") \
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

    ## Читаем данные
    events = spark.read.parquet(f'{base_input_path}')\
        .filter(F.col("date") <= F.lit(date)) \
        .withColumn('event_time', F.coalesce('event.message_ts', 'event.datetime'))\
        .withColumn('user_id', F.coalesce('event.user', 'event.message_from', 'event.reaction_from')) \
        .select('user_id', 'date', 'event_time', 'event_type')

    window =  Window().partitionBy("user_id").orderBy(F.col("event_time").asc())

    registrations = events \
        .withColumn("rank", F.row_number().over(window)) \
        .filter(F.col("rank") == 1) \
        .withColumn("event_type", F.lit("registration"))\
        .select("user_id", "date" ,"event_time", "event_type")
    
    geo = spark.read.options(delimiter=';', header=True).csv(city_geo_path)
    geo = geo.select(F.col('id'), F.col('city').alias('act_city'))

    actual_cities = spark.read.parquet(f'{actual_cities_path}/date={date}') 
    act_city = actual_cities.join(geo, 'act_city', 'left') \
        .select(F.col('user_id'), F.col('id').alias('zone_id'))
    
    all_events = events.unionByName(registrations)

    events_cities = all_events.join(act_city, 'user_id', 'inner')\
        .withColumn("month", F.trunc(F.col("date"), 'month')) \
        .withColumn("week",  F.trunc(F.col("date"), 'week'))

    events_monthly = events_cities.groupBy("zone_id", "month") \
        .pivot("event_type", ['message', 'reaction', 'subscription', 'registration']) \
        .count() \
        .withColumnRenamed('message', 'month_message') \
        .withColumnRenamed('reaction', 'month_reaction') \
        .withColumnRenamed('subscription', 'month_subscription') \
        .withColumnRenamed('registration', 'month_user')
        
    events_weekly = events_cities.groupBy("zone_id", "week") \
        .pivot("event_type", ['message', 'reaction', 'subscription', 'registration']) \
        .count() \
        .withColumnRenamed('message', 'week_message') \
        .withColumnRenamed('reaction', 'week_reaction') \
        .withColumnRenamed('subscription', 'week_subscription') \
        .withColumnRenamed('registration', 'week_user')

    result = events_monthly.join(events_weekly, "zone_id", "full").na.fill(0)
    result.repartition(1) \
        .write \
        .format('parquet') \
        .mode("overwrite") \
        .save(f"{base_output_path}/date={date}")


if __name__ == "__main__":
    main()