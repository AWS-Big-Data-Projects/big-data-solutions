
tmp = spark.read.parquet("s3://xx-xx-pds/parquet/product_category=Wireless/part-00009-495c48e6-96d6-4650-aa65-3c36a3516ddd.c000.snappy.parquet")

tmp.write.bucketBy(25,"year").saveAsTable("reviewsamazon")

spark.sql("insert into reviewstest select * from  reviewsamazon")


Spark Supported bucketed table:

CREATE TABLE `reviewstest` (`marketplace` STRING, `customer_id` STRING, `review_id` STRING, `product_id` STRING, `product_parent` STRING, `product_title` STRING, `star_rating` INT, `helpful_votes` INT, `total_votes` INT, `vine` STRING, `verified_purchase` STRING, `review_headline` STRING, `review_body` STRING, `review_date` DATE, `year` INT)
USING parquet
OPTIONS (
  `serialization.format` '1'
)
CLUSTERED BY (year)
INTO 1000 BUCKETS



Hive Supported bucketed table:

CREATE TABLE `reviewdist` (`marketplace` STRING, `customer_id` STRING, `review_id` STRING, `product_id` STRING, `product_parent` STRING, `product_title` STRING, `star_rating` INT, `helpful_votes` INT, `total_votes` INT, `vine` STRING, `verified_purchase` STRING, `review_headline` STRING, `review_body` STRING, `review_date` DATE, `year` INT)

CLUSTERED BY (year)
INTO 256 BUCKETS
stored as parquet



dataframe
  .withColumn("bucket", pmod(hash($"bucketColumn"), lit(numBuckets)))
  .repartition(numBuckets, $"bucket")
  .write
  .format(fmt)
  .bucketBy(numBuckets, "bucketColumn")
  .sortBy("bucketColumn")
  .option("path", "/path/to/your/table")
  .saveAsTable("table_name")

  
