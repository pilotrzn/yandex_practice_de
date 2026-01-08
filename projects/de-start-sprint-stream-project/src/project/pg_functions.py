from pyspark.sql.functions import lit
from pyspark.sql.types import StringType

from configs import postgres_config


def read_from_postgresql(spark):
    subscribers_restaurant_df = spark.read \
                    .format('jdbc') \
                    .option('dbtable', 'public.subscribers_restaurants') \
                    .options(**postgres_config) \
                    .load()
    return subscribers_restaurant_df


def write_to_postgresql(df):
    df.withColumn("feedback", lit(None).cast(StringType())) \
            .write \
            .format('jdbc') \
            .options(**postgres_config) \
            .option('dbtable', 'public.subscribers_feedback') \
            .mode('append') \
            .save()


def create_subscribers_feedback_table(spark):
    spark.read \
        .format('jdbc') \
        .options(**postgres_config) \
        .option('dbtable', '(SELECT 1) AS tmp') \
        .load().write \
        .format('jdbc') \
        .options(**postgres_config) \
        .option('dbtable', 'public.subscribers_feedback') \
        .option('createTableColumnTypes', '''
            restaurant_id TEXT, adv_campaign_id TEXT, adv_campaign_content TEXT,
            adv_campaign_owner TEXT, adv_campaign_owner_contact TEXT,
            adv_campaign_datetime_start BIGINT, adv_campaign_datetime_end BIGINT,
            datetime_created BIGINT, client_id TEXT,
            trigger_datetime_created INTEGER, feedback VARCHAR
        ''') \
        .mode('ignore') \
        .save()
