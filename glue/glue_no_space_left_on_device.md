At times AWS Glue ETL Job fails with the error message : 


Apache Spark uses local disk on Glue workers to spill data from memory that exceeds the heap space defined by the spark.memory.fraction configuration parameter. During the sort or shuffle stages of a job, Spark writes intermediate data to local disk before it can exchange that data between the different workers. Jobs may fail due to the following exception when no disk space remains:

An error occurred while calling o85.pyWriteDynamicFrame. error while calling spill() on 
  org.apache.spark.util.collection.unsafe.sort.UnsafeExternalSorter@5f4bb34a : No space left on device

Most commonly, this is a result of a significant skew in the dataset that the job is processing. You can also identify the skew by monitoring the execution timeline of different Apache Spark executors using AWS Glue job metrics

When you look at the memory profile of driver and executor - you will see the execution timeline and memory profile of different executors in an AWS Glue ETL job. One of the executors is probably straggling due to processing of a large partition, and actively consumes memory for the majority of the job’s duration.


Recommendation : 

This error message is thrown whenever a Spark application tries to spill data to disk to clear memory space and the underlying disk space becomes full. If a glue job is using a worker type say : G.1X worker type, which runs your jobs in nodes with 64 GiB volumes.

The most common cause for this issue is a lack of proper parallelism: if one of your job's Spark executors receives too much data (which can be caused by data skew, or by an improper repartition operation) it will try to save the excess data that cannot fit in memory to disk (spill to disk). The easiest way to address this is to ensure all executors receive an equal amount of load, and that there's enough executors to handle your dataset.

Resolution :

1) Enable metrics logging for your job, which will let you to check how many Spark executors your ETL Job is running with.

2) Run your job again to generate metrics for it.

3) Check the number of executors (metric 'glue.driver.ExecutorAllocationManager.executors.numberAllExecutors'). 

        3a) If the metric is reporting a value lower than that, there's a partitioning issue. There's several reasons as to why this could be happening, but the easiest way to address it typically is to add a repartition call after your read operation. The number of partitions should be 4 times the number of executors you can have, so 40 in this case.

        3b) If not, your job is partitioning properly and you will need to provision more resources (workers) to handle the amount of data. In order to understand how many you can check the 'glue.driver.ExecutorAllocationManager.executors.numberMaxNeededExecutors' metric, which will tell you how many executors are needed to process your dataset with maximum parallelism.



SOLUTION :


One solution is to avoid using dataframes and use RDDs instead for repartitioning: read in the gzipped files as RDDs, repartition them so each partition is small, save them in a splittable format (for example, snappy).

from pyspark.context import SparkContext

sc = SparkContext.getOrCreate()
rdd = sc.textFile("/path/to/gzipped/files/*.gz")

# repartition into smaller chunks
rdd = rdd.repartition(numPartitions=2500)

# save 
rdd.saveAsTextFile("path/to/save",
                   compressionCodecClass="org.apache.hadoop.io.compress.SnappyCodec")


from pyspark.context import SparkContext

sc = SparkContext.getOrCreate()

rdd = sc.textFile("s3://gdelt-open-data/v2/events/20150402114500.export.csv")

rdd = rdd.repartition(numPartitions=4)

sc._jsc.hadoopConfiguration().set("mapred.output.committer.class", "org.apache.hadoop.mapred.DirectFileOutputCommitter")


rdd.saveAsTextFile("s3://aws-jupyterhubtest/csv_test_compression/new/",compressionCodecClass="org.apache.hadoop.io.compress.BZip2Codec")



