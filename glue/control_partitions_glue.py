You can control the number of files/ size-of-files being written out by choosing to reparation the data before the write. If the number of output files are many, I'd recommend calling dataframe.repartition(x) just before the write operation.  A code snippet would look like this:
''''

logs_DyF = glueContext.create_dynamic_frame.from_catalog(database="amzn_review", table_name="mydata_amazonreviews", transformation_ctx = "datasource0")
logs_DF=logs_DyF.toDF()
logs_DF.show()
print (logs_DF.show())
print ("The number of partitions in source is")
print (logs_DF.rdd.getNumPartitions())
logs_DF=logs_DF.repartition(50)

logs_DyF2=DynamicFrame.fromDF(logs_DF, glueContext, "logs_DyF2")
datasink2 = glueContext.write_dynamic_frame.from_options( frame = logs_DyF2, connection_type = "s3", connection_options = {"path": "s3://xx-xx/7017122531/output/", "partitionKeys" : ["product_category"] }, format = "parquet", transformation_ctx = "datasink2")
'''

Test the values of the X(partition number) to see if this work with your dataset. This link[2] has a reference to how you can get the number of ideal partitions:
Total input dataset size / partition size =>  number of partitions


---
[1]https://aws.amazon.com/premiumsupport/faqs/
[2]https://dzone.com/articles/apache-spark-performance-tuning-degree-of-parallel

  
  

The number of files that get written out is controlled by the parallelization of your DataFrame or RDD. So if your data is split across 10 Spark partitions you cannot write fewer than 10 files without reducing partitioning (e.g. coalesce or repartition).

Now, having said that when data is read back in it could be split into smaller chunks based on your configured split size but depending on format and/or compression.

If instead you want to increase the number of files written per Spark partition (e.g. to prevent files that are too large), Spark 2.2 introduces a maxRecordsPerFile option when you write data out. With this you can limit the number of records that get written per file in each partition. The other option of course would be to repartition.

The following will result in 2 files being written out even though it's only got 1 partition:

val df = spark.range(100).coalesce(1)
df.write.option("maxRecordsPerFile", 50).save("/tmp/foo")

