#You can use the AWS Glue logger to log any application-specific messages in the script that are sent in real time to the driver log stream.

from awsglue.context import GlueContext
from pyspark.context import SparkContext

sc = SparkContext()
glueContext = GlueContext(sc)

# Continuous logging must be Enabled in the job definition for this logging
logger = glueContext.get_logger()

logger.info("info message")
logger.warn("warn message")
logger.error("error message")
