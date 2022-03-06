
import sys
import datetime
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext

args = getResolvedOptions(sys.argv,['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)

table = glueContext.create_dynamic_frame.from_options(
  "dynamodb",
  connection_options={
    "dynamodb.input.tableName": "hello",
    "dynamodb.throughput.read.percent": "1.0"
  }
)

glueContext.write_dynamic_frame.from_options(frame = table,
  connection_type="s3",
  connection_options={"path": "s3://your-s3-bucket/ddbs3"},
  format="parquet")
