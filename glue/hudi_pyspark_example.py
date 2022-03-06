# pyspark --conf "spark.serializer=org.apache.spark.serializer.KryoSerializer" \
        --conf "spark.sql.hive.convertMetastoreParquet=false" \
        --jars /usr/lib/spark/jars/httpcore-4.4.11.jar,/usr/lib/spark/jars/httpclient-4.5.9.jar,/usr/lib/hudi/hudi-spark-bundle.jar,/usr/lib/spark/external/lib/spark-avro.jar
        

/* Hudi does supports writing to non-partitioned datasets though, But for writing to a non-partitioned Hudi dataset and performing hive table syncing, you need to set the below configurations: The source for these configurations is present here.[1] Under the section "How do I use DeltaStreamer or Spark DataSource API to write to a Non-partitioned Hudi dataset".

        HIVE_PARTITION_EXTRACTOR_CLASS_OPT_KEY="hoodie.datasource.hive_sync.partition_extractor_class"
        NONPARTITION_EXTRACTOR_CLASS_OPT_VAL="org.apache.hudi.hive.NonPartitionedExtractor"
        NONPARTITIONED_KEYGENERATOR_CLASS_OPT_VAL="org.apache.hudi.keygen.NonpartitionedKeyGenerator"
        KEYGENERATOR_CLASS_OPT_KEY="hoodie.datasource.write.keygenerator.class"
 If one tries to write a Non-Partioned Hudi Dataset without the above configurations , the spark application will fail with the error message : 
 
 20/12/12 23:09:15 ERROR HiveSyncTool: Got runtime exception when hive syncing
          org.apache.hudi.hive.HoodieHiveSyncException: Failed to sync partitions for table my_table_test

          Caused by: java.lang.IllegalArgumentException: Partition path ID1 is not in the form yyyy/mm/dd
 
 */
        
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import input_file_name
from pyspark.sql.functions import udf
from pyspark.sql.functions import concat
from pyspark.sql import Row
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import sha2
from pyspark.sql.functions import encode
from pyspark.sql.functions import asc
from pyspark.sql import functions as F


sparksession = SparkSession.builder.appName("Postgrest-parquet").getOrCreate()
sparksession.sparkContext.setLogLevel("INFO")


hudiTableName = "glue"
hudiTablePath = "s3://s3-bucket/Hudi_test/glue/"
HIVE_PARTITION_EXTRACTOR_CLASS_OPT_KEY="hoodie.datasource.hive_sync.partition_extractor_class"
NONPARTITION_EXTRACTOR_CLASS_OPT_VAL="org.apache.hudi.hive.NonPartitionedExtractor"
NONPARTITIONED_KEYGENERATOR_CLASS_OPT_VAL="org.apache.hudi.keygen.NonpartitionedKeyGenerator"
KEYGENERATOR_CLASS_OPT_KEY="hoodie.datasource.write.keygenerator.class"


inputDF=sparksession.createDataFrame(
        [
            ("100", "ABC","2015-01-01", "ID1","2015-01-01T13:51:39.340396Z"),
            ("101", "FGHJ","2015-01-01", "ID1","2015-01-01T12:14:58.597216Z"),
            ("102", "GTRE","2015-01-01", "ID2","2015-01-01T13:51:40.417052Z"),
            ("103", "BARCA","2015-01-01", "ID1","2015-01-01T13:51:40.519832Z"),
            ("104", "HELLO","2015-01-02", "ID1","2015-01-01T12:15:00.512679Z"),
            ("105", "AA","2015-01-02", "ID2","2015-01-01T13:51:42.248818Z"),
        ],
        ["id", "random","creation_date", "event_id","last_update_time"]
    )


hudiOptions = {
    'hoodie.table.name': 'glue',
    'hoodie.datasource.write.recordkey.field': 'id',
    'hoodie.datasource.write.partitionpath.field': 'event_id',
    'hoodie.datasource.write.precombine.field': 'last_update_time',
    'hoodie.datasource.hive_sync.enable':'true',
    'hoodie.datasource.hive_sync.table':'glue',
    'hoodie.datasource.hive_sync.partition_fields':'event_id',
    'hoodie.datasource.hive_sync.assume_date_partitioning':'false'
    }

inputDF.write.format("org.apache.hudi").option(HIVE_PARTITION_EXTRACTOR_CLASS_OPT_KEY,NONPARTITION_EXTRACTOR_CLASS_OPT_VAL).option(KEYGENERATOR_CLASS_OPT_KEY,NONPARTITIONED_KEYGENERATOR_CLASS_OPT_VAL).option('hoodie.datasource.write.operation', 'insert').options(**hudiOptions).mode('overwrite').save(hudiTablePath)


sparksession.stop()
