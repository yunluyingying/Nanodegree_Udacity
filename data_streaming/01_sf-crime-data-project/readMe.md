### Project: SF Crime Statistics with Spark Streaming


#### Instructions 

All these steps are running in the workspace environment. 

##### Step 1

1. Start the servers

- open a terminal and run '/usr/bin/zookeeper-server-start config/zookeeper.properties'
- open another terminal and run '/usr/bin/kafka-server-start config/server.properties'

2. Install all the necessary packages 

- open a terminal and run './start.sh'

3. Run producer

- open a terminal and run 'python kafka_server.py'

4. See if you correctly implemented the server and get the screenshot for consumer_report

- Run '/usr/bin/kafka-console-consumer --bootstrap-server localhost:9092 --topic police.calls.service --from-beginning'

##### Step 2

1. Run Streaming Application

- Run 'spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.4 --master local[*] data_stream.py'


##### Step 3

1. How did changing values on the SparkSession property parameters affect the throughput and latency of the data?

A: The SparkSession property parameters could lead to the change of 'processedRowsPerSecond' and 'inputRowsPerSecond', then affect the throughput and latency of the streaming data. 

2. What were the 2-3 most efficient SparkSession property key/value pairs? Through testing multiple variations on values, how can you tell these were the most optimal?

A: By checking the two parameters 'processedRowsPerSecond' and 'inputRowsPerSecond'
    - spark.sql.shuffle.partitions                10
    - spark.streaming.kafka.maxRatePerPartition   10
    - spark.default.parallelism                   100
