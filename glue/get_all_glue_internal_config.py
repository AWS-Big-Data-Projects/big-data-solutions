import sys
from awsglue.transforms import *
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
```
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
logger = glueContext.get_logger()

logger.info(str(sc._conf.getAll()))

iterator = sc._jsc.hadoopConfiguration().iterator()
while iterator.hasNext():
prop = iterator.next()
logger.info("key: " + prop.getKey() + "value : " + prop.getValue())
```
