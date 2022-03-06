Glue Storage Issue 

As you probably know , every time you run a Spark ETL Job Glue provisions a cluster of nodes where your code will be executed on. These nodes have a disk space of 64GB each. Whenever a Spark executor receives more data than it can hold in memory, a spill-to-disk will be initiated - which pretty much means dumping the contents of already-processed data in memory onto disk so that operations can continue happening in memory. The most probable cause for this is either data skew or improper partitioning, resulting in one of your nodes receiving much more data than the rest.

In order to verify whether that's the case or not , one can always check the CloudWatch metrics - since the Spark executor metrics are usually very revealing as to whether there is proper partitioning or not.

 However, In some cases , if the spark etl job fails in less than 5 min you won't see any executor metrics , because they are generated every 5 minutes and the job runs less then 5 min & fails.

Recommendations:

      1. Evaluate how much data each value in the partition key used as the parameter for 'parittionBy' has. You are probably having a lot of data for some values, and not so much data for other ones (what is known as data skew). What I would recommend is creating a Glue Development Endpoint [1] and using it to run each code statement step by step, retrieve the number of partitions and how they are distributed after running the partitionBy and seeing how to alter this number in real time.

      2. If there is data skew indeed, the most popular technique is to deal with it is adding key salting , basically you need to add random values to your keys that equally distribute them across different partitions.

      3. Alternatively, you could consider using larger worker types so that each individual node has more memory space to hold your dataset. This will decrease the overall amount of Spark executors, but it will make each one of them larger in memory.
