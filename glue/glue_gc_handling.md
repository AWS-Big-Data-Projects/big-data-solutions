The Spark UI marks executors in red if they have spent too much time doing GC. This is determined after one checks the Spark executors which are spending a significant amount of CPU cycles performing garbage collection. Spark will mark an executor in red if the executor has spent more than 10% of the time in garbage collection than the task time as you can see in the attached snapshot.

Some of the spark tasks will be taking longer duration to execute in comparison to others. In all likelihood, this is an indication that your dataset is skewed.If skew is at the data source level (e.g. a hive table is partitioned on _month key and table has a lot more records for a particular _month),  this will cause skewed processing in the stage that is reading from the table.In such a case restructuring the table with a different partition key(s) helps. However, sometimes it is not feasible as the table might be used by other data pipelines in an enterprise. 

In such cases, there are several things that we can do to avoid skewed data processing.

  1. Data Broadcast - 

      If we are doing a join operation on a skewed dataset one of the tricks is to increase the “spark.sql.autoBroadcastJoinThreshold” value so that smaller tables get broadcasted. This should be done to ensure sufficient driver and executor memory.

  2. Data Preprocess - 

        If there are too many null values in a join or group-by key they would skew the operation. Try to preprocess the null values with some random ids and handle them in the application.

 Other Recommendations ( please take a look at the below recommendations and apply those are applicable ) : 

 
  3. Another thumb rule of spark while reading the input datasets please read the data only which is required. 

        If there are certain attributes(columns) in the sourced which are not required in the output datasets - please drop/filter them in the first place. or there might be certain attributes which are used as a look-up/Reference - once these are used you can drop them early rather than taking them until the end write them in the output. This will save overall execution time and the memory on the driver and the executors

  4. Too many small files or some large files in input ? 

        The input datasets as a general practice should not contain too many small file like in Kb's or MB's or few large files like in GB's. The number of input files for the datasets must be good in size and fairly distributed across the partitions.

  5. Partitioning the data during writes to s3 =>> 

        In general, you should select columns for partitionKeys that are of lower cardinality and are most commonly used to filter or group query results. For example, when analyzing AWS CloudTrail logs, it is common to look for events that happened between a range of dates. Therefore, partitioning the CloudTrail data by year, month, and day would improve query performance and reduce the amount of data that you need to scan to return the answer.

        The benefit of output partitioning is two-fold. First, it improves execution time for end-user queries. Second, having an appropriate partitioning scheme helps avoid costly Spark shuffle operations in downstream AWS Glue ETL jobs when combining multiple jobs into a data pipeline. For more information, see Working with partitioned data in AWS Glue.


  6. Data Persisting : 

        If you have repetitions from your SQL plan, you can persist the DataFrame so the subsequent processing could use a materialized data. You can either use df.cache() and df.persist(level). They are doing the same thing, it’s just different levels. When the workflow finished, remember to clean up by calling df.unpersist(). Spark is not smart enough to automatically clean up the data for you. I do see in some of the stages the data is being re-used multiple times - the data persisting can certainly help you to reduce the GC time overall with the spark tasks.

  7. Join Optimization: 

        Boradcast join if possible, but do not over use it. Broadcast join is a good technique to speed up the join.A few things you need to pay attention when use broadcast join.

        DataFrame is bigger than the driver node’s available working memory.
        DataFrame is bigger than executor’s available working memory.

8. Avoid Expensive Operations

        Try to avoid the following expensive operations:

            1. repartition(). Use coalesce() or shuffle partition count instead.
            2. count(). Do not call it unless you need.
            3. distinctCount(). Use approxCountDistinct() instead if you can tolerate 5% error.
            4. If distincts are required, put them in the right place.
            5. Use dropDuplicates() and use it before join and groupBy.
