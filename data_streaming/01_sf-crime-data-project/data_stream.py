import logging
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as psf
import time


# TODO Create a schema for incoming resources
schema = StructType([
    StructField('crime_id', StringType(), True),
    StructField('original_crime_type_name', StringType(), True),
    StructField('report_date', StringType(), True),
    StructField('call_date', StringType(), True),
    StructField('offense_date', StringType(), True),
    StructField('call_time', StringType(), True),
    StructField('call_date_time', TimestampType(), True),
    StructField('disposition', StringType(), True),
    StructField('address', StringType(), True),
    StructField('city', StringType(), True),
    StructField('state', StringType(), True),
    StructField('agency_id', StringType(), True),
    StructField('address_type', StringType(), True),
    StructField('common_location', StringType(), True),   
])

def run_spark_job(spark):

    # TODO Create Spark Configuration
    # Create Spark configurations with max offset of 200 per trigger
    # set up correct bootstrap server and port
    df = spark \
        .readStream \
        .format('kafka') \
        .option('kafka.bootstrap.servers', 'localhost:9092') \
        .option('subscribe', 'police.calls.service') \
        .option('startingOffsets', 'earliest') \
        .option('maxOffsetsPerTrigger', 200) \
        .option('maxRatePerPartition', 200) \
        .option('stopGracefullyOnShutdown', 'true') \
        .load()

    # Show schema for the incoming resources for checks
    df.printSchema()
    
    # TODO extract the correct column from the kafka input resources
    # Take only value and convert it to String
    kafka_df = df.selectExpr("CAST(value AS STRING)")

    service_table = kafka_df\
        .select(psf.from_json(psf.col('value'), schema).alias("DF"))\
        .select("DF.*")

    # TODO select original_crime_type_name and disposition
    distinct_table = service_table.select('original_crime_type_name', 'disposition', 'call_date_time') \
                                  .distinct() 
        
    agg_df = distinct_table\
        .select("original_crime_type_name", "call_date_time")\
        .withWatermark("call_date_time", '60 minutes')\
        .groupBy(psf.window(psf.col("call_date_time"), "10 minutes", "5 minutes"), psf.col("original_crime_type_name"))\
        .count()
    
    # TODO Q1. Submit a screen shot of a batch ingestion of the aggregation
    # TODO write output stream
    query = agg_df \
            .writeStream \
            .format('console') \
            .option("truncate", "false") \
            .outputMode('append') \
            .trigger(processingTime = "10 seconds") \
            .start()


    # TODO attach a ProgressReporter
    query.awaitTermination()
    
   
    # TODO get the right radio code json path
    radio_code_json_filepath = "radio_code.json"
    radio_code_df = spark.read.json(radio_code_json_filepath, multiLine=True)

    # clean up your data so that the column names match on radio_code_df and agg_df
    # we will want to join on the disposition code

    # TODO rename disposition_code column to disposition
   
    radio_code_df = radio_code_df.withColumnRenamed("disposition_code", "disposition")

    # TODO join on disposition column
    
    agg_df_disposition = distinct_table.select("disposition", "call_date_time")\
        .withWatermark("call_date_time", '60 minutes')\
        .groupBy(psf.window(psf.col("call_date_time"), "10 minutes", "5 minutes"), psf.col("disposition"))\
        .count()

  
    join_table = agg_df_disposition.join(radio_code_df, 'disposition', how = "left_outer")
    
    join_query = join_table \
            .writeStream \
            .format('console') \
            .outputMode('append') \
            .trigger(processingTime = "10 seconds") \
            .start()

    join_query.awaitTermination()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    # TODO Create Spark in Standalone mode
    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .appName("KafkaSparkStructuredStreaming") \
        .config("spark.ui.port", 3000) \
        .getOrCreate()

    logger.info("Spark started")

    run_spark_job(spark)

    spark.stop()
