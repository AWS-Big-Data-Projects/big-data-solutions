Python => 

Version 1 :

import logging

MSG_FORMAT = '%(asctime)s %(levelname)s %(name)s: %(message)s'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(format=MSG_FORMAT, datefmt=DATETIME_FORMAT)
logger = logging.getLogger(<logger-name-here>)

logger.setLevel(logging.INFO)

...

logger.info("Test log message")


Version 2 :

import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
root.info("check")


PySpark => 

sc = SparkContext()
sc.setLogLevel('DEBUG')
glueContext = GlueContext(sc)
logger = glueContext.get_logger()
logger.info('Hello Glue')

from awsglue.context import GlueContext
from pyspark.context import SparkContext



SparkScala => 

import com.amazonaws.services.glue.log.GlueLogger

object GlueApp {
  def main(sysArgs: Array[String]) {
    val logger = new GlueLogger
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
  }
}
