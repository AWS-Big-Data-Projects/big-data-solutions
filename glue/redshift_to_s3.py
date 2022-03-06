import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

## @params: [TempDir, JOB_NAME]
args = getResolvedOptions(sys.argv, ['TempDir','JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "red", table_name = "red_ishan_public_temp", redshift_tmp_dir = args["TempDir"],additional_options = {"aws_iam_role": "arn:aws:iam::150139034114:role/glue_full_access_for_s3"} )
                                                from_catalog(frame, name_space, table_name, redshift_tmp_dir="", transformation_ctx="")
datasource0.printSchema()
datasource0.show()
