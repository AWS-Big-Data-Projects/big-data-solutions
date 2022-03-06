import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import boto3

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sts_client = boto3.client('sts')
assumed_role_object=sts_client.assume_role(
    RoleArn="arn:aws:iam::123456789:role/assume-access-role ",
    RoleSessionName="AssumeRoleSession6"
)

credentials=assumed_role_object['Credentials']
aws_session_token=credentials['SessionToken']
aws_access_key_id=credentials['AccessKeyId']
aws_secret_access_key=credentials['SecretAccessKey']

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Declare 'org.apache.hadoop.fs.s3a.TemporaryAWSCredentialsProvider' as the credential provider for 's3a' URI and set those credentials for 's3a' URI. 
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider",  "org.apache.hadoop.fs.s3a.TemporaryAWSCredentialsProvider")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.session.token",  aws_session_token)
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key",  aws_access_key_id)
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", aws_secret_access_key)

#See here s3a is used in the URI instead of s3
s3_loc = "s3a://s3-bucket-in-diff-account/pathto/data/"

job = Job(glueContext)
job.init(args['JOB_NAME'], args)
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "ff-dd", table_name = "ddd", transformation_ctx = "datasource0")
applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("contactid", "int", "contactid", "int"), ("companyid", "long", "companyid", "long"), ("year", "string", "year", "string"), ("month", "string", "month", "string"), ("day", "string", "day", "string")], transformation_ctx = "applymapping1")
datasink2 = glueContext.write_dynamic_frame.from_options(frame = applymapping1, connection_type = "s3", connection_options = {"path": s3_loc}, format = "CSV", transformation_ctx = "datasink2")
job.commit()
