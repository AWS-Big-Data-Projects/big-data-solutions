Executing SQL using SparkSQL in AWS Glue

AWS Glue Data Catalog as Hive Compatible Metastore

The AWS Glue Data Catalog is a managed metadata repository compatible with the Apache Hive Metastore API. You can follow the detailed instructions here to configure your AWS Glue ETL jobs and development endpoints to use the Glue Data Catalog. You also need to add the Hive SerDes to the class path of AWS Glue Jobs to serialize/deserialize data for the corresponding formats. You can then natively run Apache Spark SQL queries against your tables stored in the Data Catalog.

The following example assumes that you have crawled the US legislators dataset available at s3://awsglue-datasets/examples/us-legislators. We’ll use the Spark shell running on AWS Glue developer endpoint to execute SparkSQL queries directly on the legislators’ tables cataloged in the AWS Glue Data Catalog.

>>> spark.sql("use legislators")
DataFrame[]
>>> spark.sql("show tables").show()
+-----------+------------------+-----------+
|   database|         tableName|isTemporary|
+-----------+------------------+-----------+
|legislators|        areas_json|      false|
|legislators|    countries_json|      false|
|legislators|       events_json|      false|
|legislators|  memberships_json|      false|
|legislators|organizations_json|      false|
|legislators|      persons_json|      false|

>>> spark.sql("select distinct organization_id from memberships_json").show()
+--------------------+
|     organization_id|
+--------------------+
|d56acebe-8fdc-47b...|
|8fa6c3d2-71dc-478...|
+--------------------+

A similar approach to the above would be to use AWS Glue DynamicFrame API to read the data from S3. The DynamicFrame is then converted to a Spark DataFrame using the toDF method. Next, a temporary view can be registered for DataFrame, which can be queried using SparkSQL. The key difference between the two approaches is the use of Hive SerDes for the first approach, and native Glue/Spark readers for the second approach. The use of native Glue/Spark provides the performance and flexibility benefits such as computation of the schema at runtime, schema evolution, and job bookmarks support for Glue Dynamic Frames.

>>> memberships = glueContext.create_dynamic_frame.from_catalog(database="legislators", table_name="memberships_json")
>>> memberships.toDF().createOrReplaceTempView("memberships")
>>> spark.sql("select distinct organization_id from memberships").show()
+--------------------+
|     organization_id|
+--------------------+
|d56acebe-8fdc-47b...|
|8fa6c3d2-71dc-478...|
+--------------------+
