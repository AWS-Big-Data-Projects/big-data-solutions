IF you want to read all tables under any given database in the Glue Catalog and write it into S3.

And in case you are using a for loop that loops through every table, Glue processes these tables in sequence. In other words, when we loop through all tables in a given database, the next table won't be started until the previous table finished. 

In order to execute ETL for all tables concurrently, one can make use of threading library in Python. 

//
How does it work?

- Threading in python is used to run multiple threads (tasks, function calls) at the same time. Note that this does not mean that they are executed on different CPUs. 

Python threads will NOT make your program faster if it already uses 100 % CPU time. In that case, you probably want to look into parallel programming. If you are interested in parallel programming with python, please see https://wiki.python.org/moin/ParallelProcessing

Python threads are used in cases where the execution of a task involves some waiting. One example would be interaction with a service hosted on another computer, such as a webserver. Threading allows python to execute other code while waiting.

- As soon as we call with the function multiple tasks will be submitted in parallel to spark executor from pyspark-driver at the same time and spark executor will execute the tasks in parallel provided we have enough cores

**Note this will work only if we have required executor cores to execute the parallel tasks.
//

There are the below two tested scenarios:

1. A Glue job using for loop to iterate over tables

2. A Glue job  that makes use of threading library in Python to run multiple threads (tasks, function calls) at the same time

Then check the Spark UI for both jobs to see the difference. 

Option 1: For Loop Code snippet ->

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import boto3
## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
aws_region = "us-east-1"
glue_database = "mydb"
s3_prefix = "s3://<YOURBUCKET>/PREFIX/"
    
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
client = boto3.client(service_name='glue', region_name=aws_region)
responseGetTables = client.get_tables(DatabaseName=glue_database)
tableList = responseGetTables['TableList']
tables = []
for tableDict in tableList:
    #if tableDict['Name'].startswith('PROD_'):
        tables.append(tableDict['Name'])
for table in tables:
    datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "mydb", table_name = table, transformation_ctx = "datasource0")
    #applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("code", "string", "code", "string"), ("name", "string", "name", "string"), ("id", "int", "id", "int"), ("department", "string", "department", "string"), ("article", "string", "article", "string")], transformation_ctx = "applymapping1")
    #resolvechoice2 = ResolveChoice.apply(frame = applymapping1, choice = "make_struct", transformation_ctx = "resolvechoice2")
    #dropnullfields3 = DropNullFields.apply(frame = resolvechoice2, transformation_ctx = "dropnullfields3")
    #datasink4 = glueContext.write_dynamic_frame.from_options(frame = dropnullfields3, connection_type = "s3", connection_options = {"path": s3_prefix + table}, format = "parquet", transformation_ctx = "datasink4")
    datasink4 = glueContext.write_dynamic_frame.from_options(frame = datasource0, connection_type = "s3", connection_options = {"path": s3_prefix + table}, format = "parquet", transformation_ctx = "datasink4")
   
job.commit() 

Option 2# Code snippet -> https://en.wikibooks.org/wiki/Python_Programming/Threading

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import boto3

sc = SparkContext()
glueContext = GlueContext(sc)

client = boto3.client(service_name='glue', region_name="us-east-1")
responseGetTables = client.get_tables(DatabaseName="mydb")
tableList = responseGetTables['TableList']
tables = []
for tableDict in tableList:
    tables.append(tableDict['Name'])
    
print(tables)

import threading
def run_item(f, item):
    result_info = [threading.Event(), None]
    def runit():
        result_info[1] = f(item)
        result_info[0].set()
    threading.Thread(target=runit).start()
    return result_info


def gather_results(result_infos):
    results = [] 
    for i in range(len(result_infos)):
        result_infos[i][0].wait()
        results.append(result_infos[i][1])
    return results

import time
def proc(item):
    time.sleep(1.0)
    datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "mydb", table_name = item, transformation_ctx = "datasource0")
    datasink4 = glueContext.write_dynamic_frame.from_options(frame = datasource0, connection_type = "s3", connection_options = {"path": "s3://<YOUR_BUCKET_NAME>/"+item }, format = "csv")

    return item
print(gather_results([run_item(proc, item) for item in tables]))





