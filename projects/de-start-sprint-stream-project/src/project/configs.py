from pyspark.sql.types import StructType, StructField, StringType, LongType

TOPIC_NAME_IN = 'grant5518_in'
TOPIC_NAME_OUT = 'grant5518_out'

spark_jars_packages = ",".join(
        [
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0",
            "org.postgresql:postgresql:42.4.0",
        ]
    )

incomming_message_schema = StructType([
            StructField("restaurant_id", StringType(), nullable=True),
            StructField("adv_campaign_id", StringType(), nullable=True),
            StructField("adv_campaign_content", StringType(), nullable=True),
            StructField("adv_campaign_owner", StringType(), nullable=True),
            StructField("adv_campaign_owner_contact", StringType(), nullable=True),
            StructField("adv_campaign_datetime_start", LongType(), nullable=True),
            StructField("adv_campaign_datetime_end", LongType(), nullable=True),
            StructField("datetime_created", LongType(), nullable=True),
        ])

kafka_options = {
    'kafka.bootstrap.servers': 'rc1b-2erh7b35n4j4v869.mdb.yandexcloud.net:9091',
    'kafka.security.protocol': 'SASL_SSL',
    'kafka.sasl.jaas.config': 'org.apache.kafka.common.security.scram.ScramLoginModule required username="de-student" password="ltcneltyn";',
    'kafka.sasl.mechanism': 'SCRAM-SHA-512',
    'kafka.ssl.ca.location': '/lessons/project/CA.pem',
    'kafka.sasl.username': 'de-student',
    'kafka.sasl.password': 'ltcneltyn'
}

postgres_config = {
   'url': 'jdbc:postgresql://rc1a-fswjkpli01zafgjm.mdb.yandexcloud.net:6432/de',
   'driver': 'org.postgresql.Driver',
   'user': 'student',
   'password': 'de-student'
}
