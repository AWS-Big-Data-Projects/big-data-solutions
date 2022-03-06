import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import datetime
import boto3


args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


datasource0 = glueContext.create_dynamic_frame_from_options("s3", {'paths': ["s3://xxx-xx-logs/Glue/parquet_sample_dataset/"]}, format="parquet",transformation_ctx = "datasource0")



datasink3 = glueContext.write_dynamic_frame.from_options(frame = datasource0, connection_type = "s3", connection_options = {"path": "s3://xx-xx-logs/Glue/glue_bm_issue_11_12/"}, format = "parquet",transformation_ctx = "datasink3")



job.commit()
