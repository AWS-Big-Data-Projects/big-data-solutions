spark-submit --master yarn --deploy-mode cluster --executor-memory 4g --conf spark.executor.memoryOverhead=512 demo.py

 --core comes from  --conf spark.executor.cores=4.
 
 spark-submit --deploy-mode cluster --master yarn --conf spark.executor.cores=4 demo.py 

The number of cores is entirely depends on the parameter spark.executor.cores or --executor-cores . As long one defines it in the /etc/spark/conf/spark-defaults.conf  it will pick up the default value 
from this file or if you want to change this value per application , please pass it using spark-submit as mentioned above.


Starting PySpark-shell interactively with more memory etc.

pyspark --executor-cores 5 --executor-memory 36g --driver-memory 36g --driver-cores 5
