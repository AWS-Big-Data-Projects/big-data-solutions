# Boilerplate script into the development endpoint notebook or a Glue ETL script to import the AWS Glue libraries that you need, and set up a single GlueContext: 

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

glueContext = GlueContext(SparkContext.getOrCreate())
