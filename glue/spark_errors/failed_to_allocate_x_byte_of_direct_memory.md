
This occurs due to running out of direct memory problem for the spark executors , The problem usually occurs at the shuffle read stage when there is a very large block due to a severe data skew on the shuffle write side. This problem usually occurs in a large number of shuffle operation, the task failed, and then re-implementation, has been circulating until the application failed.


https://dzone.com/articles/four-common-reasons-for-fetchfailed-exception-in-a

https://stackoverflow.com/questions/60808693/spark-shuffle-memory-error-failed-to-allocate-direct-memory


https://splice.atlassian.net/browse/SPLICE-2349

https://gankrin.org/fix-spark-error-org-apache-spark-shuffle-fetchfailedexception-too-large-frame/

https://docs.qubole.com/en/latest/troubleshooting-guide/spark-ts/troubleshoot-spark.html





Ref:

[1] https://spark.apache.org/docs/2.3.0/api/java/org/apache/spark/FetchFailed.html

