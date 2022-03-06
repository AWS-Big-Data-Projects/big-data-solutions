import pyspark
from pyspark import SparkContext
sc =SparkContext()
import sys
from awsglue.utils import getResolvedOptions
import pg8000 as redshift

args = getResolvedOptions(sys.argv,
                          ['JOB_NAME',
                           's3_bucket',
                           'config',
                           'password'])

print(args['s3_bucket'])
print(args['config'])
print(args['password'])
