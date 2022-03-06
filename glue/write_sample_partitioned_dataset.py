import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import unix_timestamp
from pyspark.sql.functions import from_unixtime
from pyspark.sql.functions import isnan, when, count, col
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import SparkSession
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(job_name, args)



df = sqlContext.createDataFrame([
         (7,"ishan","kompressor","mbenz"),
         (14,"john","wrangler","jeep"),],
         ["HOUR","NAME","car","brand"])


df.write.parquet("s3://xx-xx-xx/Glue/oge/cars/")

datasource0 = glueContext.create_dynamic_frame_from_options("s3", {'paths': ["s3://xx-xx-xx/Glue/ogenew/"], "recurse":True}, format="parquet",transformation_ctx = "datasource0")


datasink2 = glueContext.write_dynamic_frame.from_options(frame = datasource0, connection_type = "s3", connection_options = {"path": "s3://xx-xx-xx/Glue/ogenew_pp/", "partitionKeys": ["brand","car"]}, format = "parquet",transformation_ctx = "datasink2")

df = sqlContext.createDataFrame([
          (2019,10,7,7,"ishan","chicago"),
          (2018,11,8,9,"james","italy"),
          (2017,12,9,14,"john","plano"),
          (2016,1,10,13,"adam","texas"),
          (2015,2,11,12,"chris","mexico"),
          (2014,3,12,22,"niel","portland"),],
          ["YEAR","MONTH","DAY","HOUR","NAME","CITY"])

df.write.parquet("/aws-xx-logs/Glue/glue_bookmark_issue_non_partitioned/")


 datasource0 = glueContext.create_dynamic_frame_from_options("s3", {'paths': ["s3://aws-xx-logs/Glue/glue_bookmark_issue_non_partitioned/"], "recurse":True}, format="parquet",transformation_ctx = "datasource0")
       datasource0.show()
        datasource0.printSchema()
      
datasink2 = glueContext.write_dynamic_frame.from_options(frame = datasource0, connection_type = "s3", connection_options = {"path": "s3://aws-xx-logs/Glue/glue_bookmark_issue_partitioned/", "partitionKeys": ["YEAR","MONTH","DAY","HOUR"]}, format = "parquet",transformation_ctx = "datasink2")

#Date partitioned

df = sqlContext.createDataFrame([
         ("7","ishan","kompressor","mbenz","honda",10.2,"hello","how",3,11.1,11.2,11.3,11.4,11.5,"10-20-2020"),
         ("8","rajat","komp","mb","ho",123.2,"bye","wow53",55,55.2,55.3,55.4,55.5,55.6,"11-20-2020"),],
         ["cusip","sym_cd","bsym_id","issuer_nm","scrty_ds","cpn_rt","mtrty_dt","num_trades","tot_qty_opb","high_price","low_price","median_px","vwap_px","px_stand_dev_vw","date"])
