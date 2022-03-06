//spark-shell --conf "spark.serializer=org.apache.spark.serializer.KryoSerializer" --conf "spark.sql.hive.convertMetastoreParquet=false" --jars /usr/lib/hudi/hudi-spark-bundle.jar,/usr/lib/spark/external/lib/spark-avro.jar

import org.apache.hudi.DataSourceWriteOptions
import org.apache.hudi.config.HoodieWriteConfig
import org.apache.hudi.hive.MultiPartKeysValueExtractor
import org.apache.spark.sql.SaveMode
import org.apache.spark.sql.functions._

// Read data from S3 and create a DataFrame with Partition and Record Key

val inputDF = spark.read.format("parquet").load("s3://<your-s3-bucket>/<parquet-data>/")
val df1 = inputDF.select("timeperiod","flow1","occupancy1")

//Specify common DataSourceWriteOptions in the single hudiOptions variable
val hudiOptions = Map[String,String](
  HoodieWriteConfig.TABLE_NAME → "my_hudi_table",
  DataSourceWriteOptions.RECORDKEY_FIELD_OPT_KEY -> "timeperiod",
  DataSourceWriteOptions.PARTITIONPATH_FIELD_OPT_KEY ->"flow1",
  DataSourceWriteOptions.PRECOMBINE_FIELD_OPT_KEY -> "occupancy1"
)

// Write a DataFrame as a Hudi dataset
df1.write.format("org.apache.hudi").option(DataSourceWriteOptions.OPERATION_OPT_KEY, DataSourceWriteOptions.INSERT_OPERATION_OPT_VAL).options(hudiOptions).mode(SaveMode.Overwrite).save("s3://<your-s3-bucket>/myhudidataset/")
