There is no sure shot solution to handle data skewness issue as we know. 

    1. Run Spark application with spark 3.x which supports Adaptive query execution (AQE) i.e. query re-optimization that occurs during query execution  . This might give better performance in terms of comparison to spark 2.x .More on AQE -  https://docs.databricks.com/spark/latest/spark-sql/aqe.html#dataframeexplain

    2. You will need to improve your job's partition count. A simple tool is to run a 'repartition' method on your Spark DF to check where the partition count is low.

    3. Evaluate how much data each value in the partition key used as the parameter for 'parittionBy' has. You are probably having a lot of data for some values, and not so much data for other ones (what is known as data skew). What I would recommend is run code interactively nd using it to run each code statement step by step, retrieve the number of partitions and how they are distributed after running the partitionBy and seeing how to alter this number in real time.

    4. The most popular technique is to deal with it is adding key salting , basically you need to add random values to your keys that equally distribute them across different partitions.Check out these  article for salting technique and to understand skewness problem in spark.

Reference : 

1.https://itnext.io/handling-data-skew-in-apache-spark-9f56343e58e8 
2.https://www.davidmcginnis.net/post/spark-job-optimization-dealing-with-data-skew 
3.https://michaelheil.medium.com/understanding-common-performance-issues-in-apache-spark-deep-dive-data-skew-e962909f3d07
