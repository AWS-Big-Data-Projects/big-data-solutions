Problem: In Spark, wondering how to stop/disable/turn off INFO and DEBUG message logging to Spark console, when I run a Spark or PySpark program on a cluster or in my local, I see a lot of DEBUG and INFO messages in console and I wanted to turn off this logging.


Solution: By default, Spark log configuration has set to INFO hence when you run a Spark or PySpark application in local or in the cluster you see a lot of Spark INFo messages in console or in a log file.

With default INFO logging, you will see the Spark logging message like below

Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
20/03/29 17:38:24 INFO SparkContext: Running Spark version 2.4.4
20/03/29 17:38:24 INFO SparkContext: Submitted application: SparkByExamples.com


On DEV and QA environment it’s okay to keep the log4j log level to INFO or DEBUG mode. But, for UAT, live or production application we should change the log level to WARN or ERROR as we do not want to verbose logging on these environments.

Now, Let’s see how to stop/disable/turn off logging DEBUG and INFO messages to the console or to a log file. 


Using sparkContext.setLogLevel() method you can change the log level to the desired level. Valid log levels include: ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN

In order to stop DEBUG and INFO messages change the log level to either WARN, ERROR or FATAL. For example, below it changes to ERORR

      val spark:SparkSession = SparkSession.builder()
          .master("local[1]")
          .appName("SparkByExamples.com")
          .getOrCreate()

        spark.sparkContext.setLogLevel("ERROR")

With the last statement from the above example, it will stop/disable DEBUG or INFO messages in the console and you will see ERROR messages along with the output of println() or show(),printSchema() of the DataFrame methods
