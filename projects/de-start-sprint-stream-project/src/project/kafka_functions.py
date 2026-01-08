from pyspark.sql.functions import from_json, to_json, col, struct, current_timestamp, unix_timestamp
from pyspark.sql.types import StringType
from configs import (
    incomming_message_schema,
    kafka_options,
    TOPIC_NAME_IN,
    TOPIC_NAME_OUT
)


def read_from_kafka(spark):
    # читаем из топика Kafka сообщения с акциями от ресторанов
    restaurant_read_stream_df = spark.readStream \
        .format('kafka') \
        .options(**kafka_options) \
        .option('subscribe', TOPIC_NAME_IN) \
        .load()
    return restaurant_read_stream_df


def write_to_kafka(df):
    out_mess = df.withColumn \
        ('value',
         to_json(
             struct(
                col('restaurant_id'),
                col('adv_campaign_id'),
                col('adv_campaign_content'),
                col('adv_campaign_owner'),
                col('adv_campaign_owner_contact'),
                col('adv_campaign_datetime_start'),
                col('adv_campaign_datetime_end'),
                col('datetime_created'),
                col('client_id'),
                col('trigger_datetime_created')
                )
            )).select('value')

    out_mess.write\
        .format('kafka') \
        .options(**kafka_options) \
        .option('topic', TOPIC_NAME_OUT) \
        .option("checkpointLocation", "query")\
        .option("truncate", False)\
        .save()


def deserialize_df(df):
    # определяем схему входного сообщения для json
    current_timestamp_utc = unix_timestamp(current_timestamp())

    # десериализуем из value сообщения json и фильтруем по времени старта и окончания акции
    filtered_read_stream_df = df\
        .select(col("value").cast(StringType()).alias("value_str"))\
        .withColumn("deserialized_value",
                    from_json(
                        col("value_str"),
                        schema=incomming_message_schema))\
        .select("deserialized_value.*")\
        .filter(
            (col("adv_campaign_datetime_start") <= current_timestamp_utc) &
            (col("adv_campaign_datetime_end") >= current_timestamp_utc))
    return filtered_read_stream_df

