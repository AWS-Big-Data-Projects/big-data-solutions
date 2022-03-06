About the behavior regarding the requested memory and memory showing up on the spark UI sometime does not match . That's an expected behavior.The memory requested with spark-submit is considered an Upper limit for the application because if the other applications are running on the same cluster those can share. but in case where nothing is running and the cluster is sitting idle . YARN still decides using internal algorithm i.e.  How much memory to allocate to the executors and other daemons which runs in the background and support application execution . 

Check out these two stackoverflow posts that I found clarifies some of our doubts : 

1. https://stackoverflow.com/questions/38347036/spark-on-yarn-less-executor-memory-than-set-via-spark-submit
2. https://stackoverflow.com/questions/13988328/java-memory-runtime-getruntime-maxmemory/13988748#13988748 
3. https://spoddutur.github.io/spark-notes/distribution_of_executors_cores_and_memory_for_spark_application.html
