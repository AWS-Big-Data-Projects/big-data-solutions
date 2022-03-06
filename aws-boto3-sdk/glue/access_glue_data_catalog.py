import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.context import SparkConf
from pyspark.sql import SparkSession
from awsglue.context import GlueContext
from pyspark.sql import HiveContext
from pyspark.sql import SQLContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
## @params: [JOB_NAME]

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc= SparkContext()
spark=SparkSession.builder.config("hive.metastore.client.factory.class", "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory").enableHiveSupport().getOrCreate()
glueContext = GlueContext(sc)

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

spark.sql("SHOW DATABASES").show()
spark.sql("use test")
spark.sql("show tables").show()

job.commit()
