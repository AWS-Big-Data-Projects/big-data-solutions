import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job


args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()

## Set the Glue Logging level to Debug
sc.setLogLevel("DEBUG")

glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
