Glue sometimes can failed with the error message i.e. 

Container killed by YARN for exceeding memory limits. 5.7 GB of 5.5 GB physical memory used.

I can confirm the glueetl job fails with the above error because of Spark executor primarily out-of-memory exceptions - basically one of the Spark executors is receiving too much data, causing its memory to overflow and the underlying resource manager (YARN) to kill it. This usually happens 4 different times for the same Spark task, which as per the default configuration caused the entire job to be aborted.

Executor out-of-memory exceptions are typically caused by data skew: when your dataset's not properly distributed across all your Spark executors, some receive more data than others. If this imbalance is large enough, one of the executors can receive enough data to overflow its memory as I described before.

This is quite easy to identify by checking your job run's Spark executor count: since Glue ETL jobs use Spark's dynamic executor allocation, the number of active executors at any given time is directly proportional to the number of Spark partitions your dataset has (though the number of pending tasks) - so a low executor count indicates improper partitioning which can be addressed.


I can recommend:

* Enable metrics logging for your ETL job whcih lets you to check your job's metrics to analyze failures such as this one in the future.

* Once metrics have been enabled, run your job again. When you encounter the same issue, check your job's Executor count metric (glue.driver.ExecutorAllocationManager.executors.numberAllExecutors). Given that your job is running with n number of DPUs of the Standard worker type, you could have up to n + 1 executors. If the number you are getting is any lower than that, there is some issue in your job's partition count.

** If there is such an issue, you will need to improve your job's partition count. There are many possible causes here that I cannot identify without knowing more about your job's environment, but a simple tool is to run a 'repartition' method [1] on your DynamicFrame at the moment where the partition count is low.

** If there is not such an issue, your dataset is being properly partitioned and your nodes are simply not powerful enough to handle the volume of data. You can either add additional nodes (by increasing the number of DPUs your job has) or use a larger worker type [2] so that your executors have additional memory space.

Reference :


[1] https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html#aws-glue-api-crawler-pyspark-extensions-dynamic-frame-repartition
[2] https://aws.amazon.com/about-aws/whats-new/2019/04/aws-glue-now-supports-additional-configuration-options-for-memory-intensive-jobs/
