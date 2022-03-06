import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import boto3
from botocore.exceptions import ClientError

glueContext = GlueContext(SparkContext.getOrCreate())

df1 = glueContext.create_dynamic_frame.from_catalog(database = "db111111", table_name = "json", transformation_ctx = "df1")

MARKET_SHARE_FORECAST_MAPPINGS = [
    ("year",               "bigint", "year",               "bigint"),
    ("forecast",           "double", "forecast",           "decimal"),
    ("actual",             "double", "actual",             "decimal"),
    ("producer",           "string", "producer",           "string"),
    ("market",             "string", "market",             "string"),
    ("loadyear",           "string", "loadyear",           "int"),
    ("loadmonth",          "string", "loadmonth",          "int"),
    ("loadday",            "string", "loadday",            "int")
]

#before apply mapping
df1.toDF().show()
+--------+---------+-------+----+-------------+------+--------+------+
|loadyear|loadmonth|loadday|year|     forecast|actual|producer|market|
+--------+---------+-------+----+-------------+------+--------+------+
|    2020|       06|     07|2010|0.30275518551| 0.297| Belarus|Brazil|
|    2020|       06|     07|2011|0.34575518551|  0.34| Belarus|Brazil|
+--------+---------+-------+----+-------------+------+--------+------+

df1.printSchema()

root
|-- loadyear: string
|-- loadmonth: string
|-- loadday: string
|-- year: int
|-- forecast: double
|-- actual: double
|-- producer: string
|-- market: string

apply_mapping = ApplyMapping.apply(
            frame=df1,
            mappings=MARKET_SHARE_FORECAST_MAPPINGS,
            transformation_ctx='df2')

apply_mapping.printSchema()

root
|-- year: long
|-- forecast: decimal
|-- actual: decimal
|-- producer: string
|-- market: string
|-- loadyear: int
|-- loadmonth: int
|-- loadday: int

#after applymapping where precision=10,scale=2 by default.

apply_mapping.toDF().show()

+----+--------+------+--------+------+--------+---------+-------+
|year|forecast|actual|producer|market|loadyear|loadmonth|loadday|
+----+--------+------+--------+------+--------+---------+-------+
|null|    0.30|  0.30| Belarus|Brazil|    2020|        6|      7|
|null|    0.35|  0.34| Belarus|Brazil|    2020|        6|      7|
+----+--------+------+--------+------+--------+---------+-------+


MARKET_SHARE_FORECAST_MAPPINGS = [
    ("year",               "bigint", "year",               "bigint"),
    ("forecast",           "double", "forecast",           "decimal(11,11)"),
    ("actual",             "double", "actual",             "decimal"),
    ("producer",           "string", "producer",           "string"),
    ("market",             "string", "market",             "string"),
    ("loadyear",           "string", "loadyear",           "int"),
    ("loadmonth",          "string", "loadmonth",          "int"),
    ("loadday",            "string", "loadday",            "int")
]

apply_mapping_final = ApplyMapping.apply(
            frame=df1,
            mappings=MARKET_SHARE_FORECAST_MAPPINGS,
            transformation_ctx='df2')

#on changing the parameter values and setting scale and precision values each to 11.
apply_mapping_final.toDF().show()
+----+-------------+------+--------+------+--------+---------+-------+
|year|     forecast|actual|producer|market|loadyear|loadmonth|loadday|
+----+-------------+------+--------+------+--------+---------+-------+
|null|0.30275518551|  0.30| Belarus|Brazil|    2020|        6|      7|
|null|0.34575518551|  0.34| Belarus|Brazil|    2020|        6|      7|
+----+-------------+------+--------+------+--------+---------+-------+

#max value for precision and scale is 38.
MARKET_SHARE_FORECAST_MAPPINGS = [
    ("year",               "bigint", "year",               "bigint"),
    ("forecast",           "double", "forecast",           "decimal(38,38)"),
    ("actual",             "double", "actual",             "decimal"),
    ("producer",           "string", "producer",           "string"),
    ("market",             "string", "market",             "string"),
    ("loadyear",           "string", "loadyear",           "int"),
    ("loadmonth",          "string", "loadmonth",          "int"),
    ("loadday",            "string", "loadday",            "int")
]

apply_mapping_final = ApplyMapping.apply(
            frame=df1,
            mappings=MARKET_SHARE_FORECAST_MAPPINGS,
            transformation_ctx='df2')

apply_mapping_final.toDF().show()

+----+--------------------+------+--------+------+--------+---------+-------+
|year|            forecast|actual|producer|market|loadyear|loadmonth|loadday|
+----+--------------------+------+--------+------+--------+---------+-------+
|null|0.302755185510000...|  0.30| Belarus|Brazil|    2020|        6|      7|
|null|0.345755185510000...|  0.34| Belarus|Brazil|    2020|        6|      7|
+----+--------------------+------+--------+------+--------+---------+-------+
===
