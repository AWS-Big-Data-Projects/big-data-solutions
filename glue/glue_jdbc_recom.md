JDBC Optimizations: Apache Spark uses JDBC drivers to fetch data from JDBC sources such as MySQL, PostgresSQL, Oracle.
    Fetchsize: By default, the Spark JDBC drivers configure the fetch size to zero. This means that the JDBC driver on the Spark executor tries to fetch all the rows from the database in one network round trip and cache them in memory, even though Spark transformation only streams through the rows one at a time. This may result in the Spark executor running out of memory with the following exception:

    WARN YarnAllocator: Container killed by YARN for exceeding memory limits. 5.5 GB of 5.5 GB physical memory used. Consider boosting spark.yarn.executor.memoryOverhead.
    WARN YarnSchedulerBackend$YarnSchedulerEndpoint: Container killed by YARN for exceeding memory limits. 5.5 GB of 5.5 GB physical memory used. Consider boosting spark.yarn.executor.memoryOverhead.
    ERROR YarnClusterScheduler: Lost executor 4 on ip-10-1-2-96.ec2.internal: Container killed by YARN for exceeding memory limits. 5.5 GB of 5.5 GB physical memory used. Consider boosting spark.yarn.executor.memoryOverhead.
    WARN TaskSetManager: Lost task 0.3 in stage 0.0 (TID 3, ip-10-1-2-96.ec2.internal, executor 4): ExecutorLostFailure (executor 4 exited caused by one of the running tasks) Reason: Container killed by YARN for exceeding memory limits. 5.5 GB of 5.5 GB physical memory used. Consider boosting spark.yarn.executor.memoryOverhead.

    In Spark, you can avoid this scenario by explicitly setting the fetch size parameter to a non-zero default value. With AWS Glue, Dynamic Frames automatically use a fetch size of 1,000 rows that bounds the size of cached rows in JDBC driver and also amortizes the overhead of network round-trip latencies between the Spark executor and database instance. The example below shows how to read from a JDBC source using Glue dynamic frames.

    val (url, database, tableName) = {
     ("jdbc_url", "db_name", "table_name")
     } 
    val source = glueContext.getSource(format, sourceJson)
    val dyf = source.getDynamicFrame

Spark’s Read Partitioning: Apache Spark by default uses only one executor to open up a JDBC connection with the database and read the entire table into a Spark dataframe. This can result in an unbalanced distribution of data processed across different executors. As a result, it is usually recommended to use a partitionColumn, lowerBound, upperBound, and numPartitions to enable reading in parallel from different executors. This allows for more balanced partitioning if there exists a column that has a uniform value distribution. However, Apache Spark restricts the partitionColumn to be one of numeric, date, or timestamp data types. For example:

val df = spark.read.jdbc(url=jdbcUrl, 
    table="employees", partitionColumn="emp_no", 
    lowerBound=1L, upperBound=100000L, numPartitions=100, 
    fetchsize=1000, connectionProperties=connectionProperties)

Glue’s Read Partitioning: AWS Glue enables partitioning JDBC tables based on columns with generic types, such as string. This enables you to read from JDBC sources using non-overlapping parallel SQL queries executed against logical partitions of your table from different Spark executors. You can control partitioning by setting a hashfield or hashexpression. You can also control the number of parallel reads that are used to access your data by specifying hashpartitions. For best results, this column should have an even distribution of values to spread the data between partitions. For example, if your data is evenly distributed by month, you can use the month column to read each month of data in parallel. Based on the database instance type, you may like to tune the number of parallel connections by adjusting the hashpartitions. For example:

glueContext.create_dynamic_frame.from_catalog(
    database = "my_database",
    tableName = "my_table_name",
    transformation_ctx = "my_transformation_context",
    additional_options = {
        'hashfield': 'month',
        'hashpartitions': '5'
    )
)

Bulk Inserts: AWS Glue offers parallel inserts for speeding up bulk loads into JDBC targets. The following example uses a bulk size of two, which allows two inserts to happen in parallel. This is helpful for improving the performance of writes into databases such as Aur.

val optionsMap = Map(
  "user" -> user,
  "password" -> pwd,
  "url" -> postgresEndpoint,
  "dbtable" -> table,
  "bulkSize" -> "2")
val options = JsonOptions(optionsMap)
val jdbcWrapper = JDBCWrapper(glueContext, options)
glueContext.getSink("postgresql", options).writeDynamicFrame(dyf)

Passing it in write_dynamic_frame.from_options:
--------------------------------------------------------
conn_opt = {"url": "jdbc:postgresql://db-cluster.cluster-xxxxxxxxxx.us-east-1.rds.amazonaws.com:5480/dbxxx?sslmode=require", "user": "postgres_usre", "password": "******", "dbtable":"public.postgrestable_name", "bulkSize":"100"} 
datasink5=glueContext.write_dynamic_frame.from_options(frame = initialsql2, connection_type = "postgresql_conn", connection_options = conn_opt)




BulkInserts with Native Spark : 

batch size can be increased from its default value of 1000, and thereby increase the performance on JDBC driver.

Batch size as a parameter is supported in spark data frame[1].  Batch size parameter is applicable only when the connection is used as a source, not as a sink [2]. The only possible connection options (for connection type 'documentdb' and 'mongodb') to tune the parameters in the JDBC DynamicFrameWriter is specified in [2].

The JDBC batch size, which determines how many rows to insert per round trip. This can help performance on JDBC drivers. This option applies only to writing. It defaults to 1000.

###############
jdbcDF = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://....") \
    .option("dbtable", "tablename") \
    .option("user", "") \
    .option("password", "") \
    .load()

jdbcDF.write \
    .format("jdbc")\
    .option("url", "jdbc:postgresql:") \
    .option("dbtable", "") \
    .option("user", "") \
    .option("password", "") \
    .option("batchsize",10000) \
    .save()
##############3

Resources:
[1] Retrieved From - https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html
[2] Retrieved From - https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect.html
https://docs.aws.amazon.com/glue/latest/dg/monitor-profile-debug-oom-abnormalities.html#monitor-profile-debug-oom-executor
Regarding numPartitons:
https://spark.apache.org/docs/2.2.0/sql-programming-guide.html#jdbc-to-other-databases



Join Optimizations: One common reason for Apache Spark applications running out of memory is the use of un-optimized joins across two or more tables. This is typically a result of data skew due to the distribution of join columns or an inefficient choice of join transforms. Additionally, ordering of transforms and filters in the user script may limit the Spark query planner’s ability to optimize. There are 3 popular approaches to optimize join’s on AWS Glue.
    Filter tables before Join: You should pre-filter your tables as much as possible before joining. This helps to minimize the data shuffled between the executors over the network. You can use AWS Glue push down predicates for filtering based on partition columns, AWS Glue exclusions for filtering based on file names, AWS Glue storage class exclusions for filtering based on S3 storage classes, and use columnar storage formats such as Parquet and ORC that support discarding row groups based on column statistics such as min/max of column values.
    Broadcast Small Tables: Joining tables can result in large amounts of data being shuffled or moved over the network between executors running on different workers. Because of this, Spark may run out of memory and spill the data to physical disk on the worker. This behavior can be observed in the following log message:

    INFO [UnsafeExternalSorter] — Thread 168 spilling sort data of 3.1 GB to disk (0 time so far)

    In cases where one of the tables in the join is small, few tens of MBs, we can indicate Spark to handle it differently reducing the overhead of shuffling data. This is performed by hinting Apache Spark that the smaller table should be broadcasted instead of partitioned and shuffled across the network. The Spark parameter spark.sql.autoBroadcastJoinThreshold configures the maximum size, in bytes, for a table that will be broadcast to all worker nodes when performing a join. Apache Spark will automatically broadcast a table when it is smaller than 10 MB. You can also explicitly tell Spark which table you want to broadcast as shown in the following example:

    val employeesDF = employeesRDD.toDF
    va departmentsDF = departmentsRDD.toDF

    // materializing the department data
    val tmpDepartments = broadcast(departmentsDF.as("departments"))

    val joinedDF = employeesDF.join(broadcast(tmpDepartments), 
       $"depId" === $"id",  // join by employees.depID == departments.id 
       "inner")

    // Show the explain plan and confirm the table is marked for broadcast
    joinedDF.explain()

    == Physical Plan ==
    *BroadcastHashJoin [depId#14L], [id#18L], Inner, BuildRight
    :- *Range (0, 100, step=1, splits=8)
    +- BroadcastExchange HashedRelationBroadcastMode(List(input[0, bigint, false]))
       +- *Range (0, 100, step=1, splits=8

PySpark User Defined Functions (UDFs): Using PySpark UDFs can turn out to be costly for executor memory. This is because data must be serialized/deserialized when it is exchanged between the Spark executor JVM and the Python interpreter. The Python interpreter needs to process the serialized data in Spark executor’s off-heap memory. For datasets with large or nested records or when using complex UDFs, this processing can consume large amounts of off-heap memory and can lead to OOM exceptions resulting from exceeding the yarn memoryOverhead. Here what the error message looks like:

ERROR YarnClusterScheduler: Lost executor 1 on ip-xxx:
Container killed by YARN for exceeding memory limits. 5.5 GB of 5.5 GB physical memory used.
Consider boosting spark.yarn.executor.memoryOverhead

Similarly, data serialization can be slow and often leads to longer job execution times. To avoid such OOM exceptions, it is a best practice to write the UDFs in Scala or Java instead of Python. They can be imported by providing the S3 Path of Dependent Jars in the Glue job configuration. Another optimization to avoid buffering of large records in off-heap memory with PySpark UDFs is to move select and filters upstream to earlier execution stages for an AWS Glue script.
Incremental processing: Processing large datasets in S3 can result in costly network shuffles, spilling data from memory to disk, and OOM exceptions. To avoid these scenarios, it is a best practice to incrementally process large datasets using AWS Glue Job Bookmarks, Push-down Predicates, and Exclusions. Concurrent job runs can process separate S3 partitions and also minimize the possibility of OOMs caused due to large Spark partitions or unbalanced shuffles resulting from data skew. Vertical scaling with higher memory instances can also mitigate the chances of OOM exceptions because of insufficient off-heap memory or Apache Spark applications that can not be readily optimized.

You can also use Glue’s G.1X and G.2X worker types that provide more memory and disk space to vertically scale your Glue jobs that need high memory or disk space to store intermediate shuffle output. Vertical scaling for Glue jobs is discussed in our first blog post of this series.
