## Option 1 :

spark-submit \
>  --conf "spark.driver.extraJavaOptions=-XX:+UseG1GC -XX:+PrintGCDetails -XX:+PrintGCTimeStamps" \
>  --conf "spark.executor.extraJavaOptions=-XX:+UseG1GC -XX:+PrintGCDetails -XX:+PrintGCTimeStamps" \
>  sample_pyspark.py

## Option 2: 

spark-submit \
 --conf "spark.driver.extraJavaOptions=-XX:+UseG1GC -XX:+PrintFlagsFinal \
 -XX:+PrintReferenceGC -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCTimeStamps \
 -XX:+PrintAdaptiveSizePolicy -XX:+UnlockDiagnosticVMOptions -XX:+G1SummarizeConcMark \
 -XX:InitiatingHeapOccupancyPercent=35 -XX:ConcGCThreads=20" \
 --conf "spark.executor.extraJavaOptions=-XX:+UseG1GC -XX:+PrintFlagsFinal -XX:+PrintReferenceGC \
 -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -XX:+PrintAdaptiveSizePolicy \
 -XX:+UnlockDiagnosticVMOptions -XX:+G1SummarizeConcMark -XX:InitiatingHeapOccupancyPercent=35 \
  -XX:ConcGCThreads=20" \
 sample_pyspark.py

# Ref:

/*
http://saucam.github.io/blog/2015/10/14/tuning-g1gc-spark/
https://databricks.com/blog/2015/05/28/tuning-java-garbage-collection-for-spark-applications.html
https://aws.amazon.com/blogs/big-data/best-practices-for-successfully-managing-memory-for-apache-spark-applications-on-amazon-emr/
https://medium.com/@sambodhi_72782/spark-tuning-manual-47b98ccb2b2c
https://community.cloudera.com/t5/Support-Questions/Spark-Job-long-GC-pauses/td-p/282690
https://stackoverflow.com/questions/34589051/garbage-collection-time-very-high-in-spark-application-causing-program-halt/34590161 (edited
*/
                                                                                                                                   
 Option 3:
 
  spark.executor.extraJavaOptions=-XX:+UseG1GC -XX:+PrintReferenceGC -XX:+PrintGCDetails --conf spark.driver.extraJavaOptions=-XX:+UseG1GC -XX:+PrintReferenceGC -XX:+PrintGCDetails
