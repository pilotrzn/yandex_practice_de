from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, unix_timestamp
from configs import spark_jars_packages

from pg_functions import (
    create_subscribers_feedback_table,
    read_from_postgresql,
    write_to_postgresql)

from kafka_functions import (
    deserialize_df,
    read_from_kafka,
    write_to_kafka
)


def spark_init():
    # создаём spark сессию с необходимыми библиотеками в spark_jars_packages для интеграции с Kafka и PostgreSQL
    spark = SparkSession.builder \
        .appName("RestaurantSubscribeStreamingService") \
        .config("spark.sql.session.timeZone", "UTC") \
        .config("spark.jars.packages", spark_jars_packages) \
        .getOrCreate()
    return spark


def foreach_batch_function(df, epoch_id):
    # сохраняем df в памяти, чтобы не создавать df заново перед отправкой в Kafka
    df.persist()
    # записываем df в PostgreSQL с полем feedback
    write_to_postgresql(df)
    # создаём df для отправки в Kafka. Сериализация в json.
    write_to_kafka(df)
    # очищаем память от df
    df.unpersist()


def main():
    spark = spark_init()
    create_subscribers_feedback_table(spark)
    restaurant_read_stream_df = read_from_kafka(spark)
    filtered_read_stream_df = deserialize_df(restaurant_read_stream_df)
    subscribers_restaurant_df = read_from_postgresql(spark)

    result_df = filtered_read_stream_df\
        .join(subscribers_restaurant_df, 'restaurant_id')\
        .withColumn("trigger_datetime_created",
                    unix_timestamp(current_timestamp()))\
        .drop('id')\
        .dropDuplicates(['client_id', 'restaurant_id'])

    result_df.writeStream \
        .foreachBatch(foreach_batch_function) \
        .start() \
        .awaitTermination()


if __name__ == "__main__":
    main()
