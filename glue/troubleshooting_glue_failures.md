Intro


A  Glue Job will fail with an error similar to the following:

OOM on Executor

JobRun Example

Diagnostics: Container [pid=123,containerID=container_123456789_0001_02_000001]
is running beyond physical memory limits. Current usage: 5.5 GB of 5.5 GB physical
memory used; 7.6 GB of 27.5 GB virtual memory used. Killing container.


An error occurred while calling o611.pyWriteDynamicFrame. ExecutorLostFailure
(executor 4 exited caused by one of the running tasks)
Reason: Executor heartbeat timed out after 153066 ms

jr_d2e40821308a19e375a8db37cf41ed9db284ae9b5ea987f8d67a3187ea0d6d18

An error occurred while calling o151.parquet. Job aborted.


OOM on Driver

JobRun Example

Command failed with exit code 1

jr_05a2b5b28ce4c6489af3823eea37692a92e59821fc4db16b5aa8725a31ef43ee



Troubleshoot Type of Failure

You need to figure out what type of OOM you dealing with.

Is the OOM on Read or Write? Tip: check container /stdout.gz
Is the failure on the Driver or Executor?
Is the issue with JDBC or S3 data movement?
If it's S3 related, what type of files?
Big files or many files?

Where to find OOM in the EMR log?
More needed here. Different failures will be seen in different logs. Most common:

Open the Cluster for the Job
Open Master Instance magnifying glass
Browse to Applications> Hadoop-Yarn> YarnResourceManger:
s3://s3-bucket/j-2ID88UCMVXF86/node/i-03d4d3e0df05a6860/applications/hadoop-yarn/yarn-yarn-resourcemanager-ip-172-31-54-187.log.gz

Search for "running beyond" or "Killing"


DPU Resources Explained
These are defaults, but container properties can be tweaked

DPU's are m4.xlarge with 16GB memory
Maximum memory per node in Yarn is 12288MB
Containers on the DPU are launched with 5GB Memory each
Containers are set with 10% memoryOverhead which is 512MB
Total memory per Container is 5.5GB
Thus, Glue launches two Containers per DPU


OOM Causes

More needed here. Different failures have different causes, more than can be covered here. Most common:

Large unsplittable files (like Parquet) result in large in-memory partitions
JDBC connections will always OOM with a large dataset as only a single connection is made to the JDBC URL. The driver tries to download the whole table to RAM at one time in on an executor. A JDBC job going over 6 DPU is useless and will almost always cause issues on the DB side. (mitczach)



Solutions & Workarounds

This is a high-level list of possible options to avert the most common the issues. 
It is a not a complete list and you need to know what OOM you are dealing with (see troubleshooting above).



1. groupFiles & groupSize

When you run a Glue ETL job Glue subdivides the work into multiple tasks which can run in parallel. --groupFiles property enables each ETL task to read a group of input files into a single in-memory partition, this is especially useful when there is a large number of small files in your S3 data store. When you set this property, you instruct Glue to group files within an S3 data partition and set the size of the groups to be read.

So to give you a specific example, if you provide the S3 path while creating the Dynamic Frame as "s3://yourbucketname/yourfilename.csv" and made "--groupFiles" enable. This will not have any impact on the performance as 'groupFiles' option is there to group multiple small files inside a partition into a single group so that all the files don't get loaded into memory at once when the partition gets processed.

On the other hand, if you provide the S3 path while creating the Dynamic Frame as "s3://yourbucketname/" and made "--groupFiles" enable. It will group the files inside a partition into chunks based on the group size provided or a calculated group size(if no group size is provided). Glue uses an internal heuristic to list and group the files.

More information: https://docs.aws.amazon.com/glue/latest/dg/grouping-input-files.html




2. Use DataFrame

If your job fails when writing DynamicFrame, you can convert to a Spark DataFrame before writing. To do this, you will write two additional code lines near the end of your script: # Requires more information

. . .
final_dataframe = my_dynframe.toDF()
dataFrame.write.format('csv').save("s3://my-glue/csv_out/")
job commit
. . .

More information on converting your DynamicFrame to a DataFrame: http://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html
(as per: 4331540191)



3. Use DynamicFrame

DynamicFrames construction doesn't require two passes over data to compute schema and then read them like Spark Dataframes. The schema is read on the fly. Data is read in lazy fasion, thus filtering can be applied before the data is really pulled.  # Requires more information




4. S3 Partitioning and Push Down Predicate

Partitioning is another method of improving resource allocation. Using a Hive-style partitioning in S3 provides better query performance with Athena because of the Predicate Pushdown benefit.  By using a predictable layout, queries are able to jump and filter to where the required data resides. The benefit of using this with Parquet files is that it gives Hive the potential to skip large portions of data, such the entries storing stats data. Below are third party articles relating to using Hive partitions with Parquet:

 - Advantage of creating Hive partitions when using parquet file storage: https://stackoverflow.com/questions/38759435/advantage-of-creating-hive-partitions-when-using-parquet-file-storage

 -  Schema Evolution with Hive and Parquet using partitioned views: http://blog.nuvola-tech.com/2017/02/schema-evolution-with-hive-and-parquet-using-partitioned-views/"

 - AWS Predictive Pushdown: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-partitions.html#aws-glue-programming-etl-partitions-pushdowns

- Code exampe: datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "testing", table_name = "data", transformation_ctx = "datasource0",push_down_predicate = "(partition_0 == '2017' and partition_1 == '01')")





5. Python threading and batch processing

Implement code to batch the dataset and thread the application. This will allow Glue to run through the data without hitting the memory limits. Making smaller batches also allows higher parallelism, making your large DPU numbers more ideal. Glue is currently designed with an Executor Memory limit of about 5.5GB. You will want to target threading to keep my JVM Memory below that.

Please see the below GitBan example from our Github about threading PySpark applications which provides an example:
https://github.com/awslabs/aws-big-data-blog/tree/master/aws-blog-spark-parquet-conversion



6. Change FetchSize for JDBC

JDBC OOM on Executor on read:

1. Fix the Fetchsize.
2. Note postgres/Redshift ignores Fetchsize on Spark 2.1 even when set manually.
3. DynamicFrame MySQL uses 1000 default. Only set on MySQL currently
4. JDBC partitioning on read: 7-10 is good. More can negate performance.
5. JDBC partitioning on write: configure batchsize

# Requires more information




7. Add More Executors

On the backend of Glue, the Spark service initiates the Executors to process data. In your job, Executors are not launched fast enough to handle all the data. We may be able to fix it by starting more Executors:
1. In the AWS Console go to Glue> Jobs > Edit Job> Script libraries and job parameters
2. In the Job parameters section, add the following:
     Key: "--conf"
     Value: "spark.dynamicAllocation.minExecutors=8"
3. Run the job again



8. Shard your Data

 Shard your source dataset and run a job for each shard. # Requires more information





11. Increase the memoryOverhead

Note: Requires more than 2 DPU's. This might cause your job to fail for new reasons. It is a considered a last resort and not supported. This is a workaround, not a solution.
By by altering the memoryOverhead of your Executor, you might be able allocate sufficient memory to complete your Job. The memory allocated on the DPU cannot go beyond 12288MB. You can thus allocate up to 1024MB memoryOverhead for for two Executor to run on the DPU, or you can go up to 7168MB for one Executor per DPU.

You can modify the memoryOverhead to be 1GB as follows:
1. Open Glue> Jobs > Edit your Job> Job parameters near the bottom
2. Set the following:
     key: --conf
    value: spark.yarn.executor.memoryOverhead=1G

You can experiment with specifying a memoryOverhead that would allocates one or two Executors per DPU. There are benefits and drawbacks to both.




12. Use DataPipeline or EMR Spark

Should you find the previously provided Glue adjustments do not solve the issue, I suggest looking into using DataPipeline with EMR to move your data. On EMR you have granular control of your Executor memory, Instance size etc. to ensure your data gets moved consistently reliably:
https://aws.amazon.com/datapipeline/


13. Spark Performance Turning

Glue is built on Spark, thus the same optimization techniques apply to Glue as to Spark. As I am sure you understand, many of these Spark configuration options are not applicable to the managed server environment of Glue, but I recommend you review the advice on the subject of performance tuning:
- https://www.indix.com/blog/engineering/lessons-from-using-spark-to-process-large-amounts-of-data-part-i/
- http://www.lewisgavin.co.uk/Spark-Performance/ 
- https://www.slideshare.net/SparkSummit/top-5-mistakes-when-writing-spark-applications-by-mark-grover-and-ted-malaska



14. Tuning Spark conf parameters

Disclaimer: This requires more than 2 DPU's and might cause your job to fail for new reasons. Changing Spark configuration parameters is considered a last resort and we will not offer further support. This is a workaround, not a solution.
Although Glue Jobs are a fully managed Spark operation, there is still the opportunity to modify the preconfigured resource variables of jobs. Using the method below, you can alter the properties such as DriverMemory, ExecutorCount and MemoryOverheard. Remember that your properties would still have to be within the allocated compute resources for the DPU. And if you plan on testing these, please do so in a non-production workload if possible:

An example of how to modify the memoryOverhead to be 1GB:
1. Open Glue> Jobs > Edit your Job> Job parameters near the bottom
2. Set the following:
     key: --conf
    value: spark.yarn.executor.memoryOverhead=1G
3. Save and run your job.

And here is the trick to pass multiple "--conf" values to a job.

- - -
Key: --conf
Value: spark.executor.memory=10G --conf spark.yarn.executor.memoryOverhead=1G
- - -

For a full list of configurable properties, see: https://spark.apache.org/docs/2.2.1/configuration.html








Useful links:

- Large collection of Spark OOM cases and solutions: https://github.com/JerryLead/MyNotes/blob/master/Grind/OOM-Cases-in-Spark-Users.md

- Glue OOM Debugging: https://docs.aws.amazon.com/glue/latest/dg/monitor-profile-debug-oom-abnormalities.html

