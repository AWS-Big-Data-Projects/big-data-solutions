import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import udf
from pyspark.sql.types import *
import re

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "default", table_name = "aaa", transformation_ctx = "datasource0")

applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("col0", "long", "aa", "long")], transformation_ctx = "applymapping1")



dropnullfields3 = DropNullFields.apply(frame = resolvechoice2, transformation_ctx = "dropnullfields3")


##### start code to add field and use partions
def extractYear(x):
    # 11/1/2014 00:00:11
    # 2019-02-01 00:00:06.2570
    #z = re.search(r"(\d{4}) |^(\d{4})", x)
    z = re.search(r"\/(\d{4})$|^(\d{4})", x)
    if z.group(1):
        return z.group(1)
    else:
        return z.group(2)
udfExtractYear = udf(extractYear, StringType())

def extractMonth(x):
    # 11/1/2014 00:00:11
    # 2019-02-01 00:00:06.2570
    z = re.search("^(\d+)\/|\-(\d+)\-", x)
    if z.group(1):
        return int(z.group(1))
    else:
        return int(z.group(2))
udfExtractMonth = udf(extractMonth, IntegerType())

def extractQuarter(x):
    # 11/1/2014 00:00:11
    # 2019-02-01 00:00:06.2570
    month = ""
    quarter = "Q1"
    z = re.search("^(\d+)\/|\-(\d+)\-", x)
    if z.group(1):
        month = int(z.group(1))
    else:
        month =  int(z.group(2))
    
    if month >=1 and month <=3:
        quarter = "Q1"
    if month >=4 and month <=6:
        quarter = "Q2"
    if month >=7 and month <=10:
        quarter = "Q3"
    if month >=10 and month <=12:
        quarter = "Q4"
    return quarter
udfExtractQuarter = udf(extractQuarter, StringType())

df = dropnullfields3.toDF()

# Filter out null number_borrowers
## df = df.filter(df.["number of borrowers"].isNotNull())

# Add some columns
df = df.withColumn("year", udfExtractYear(df["dd"]))
df = df.withColumn("month", udfExtractMonth(df["dd"]))
df = df.withColumn("quarter", udfExtractQuarter(df["dd"]))
df.printSchema()
df.show(2)

# Save it, partition.
df.write.mode("overwrite").partitionBy("year").parquet("s3://xxx/Glue/data777/")


job.commit()
