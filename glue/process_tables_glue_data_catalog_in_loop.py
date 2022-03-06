import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import datetime
import boto3
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'region', 'source_database',
                                     'target_location', 'target_prefix'])
job_name = args['JOB_NAME']
region = args['region']

source_db = args['source_database']
target_bucket = args['target_location']
target_prefix = args['target_prefix']
sc = SparkContext()
glueContext = GlueContext(sc)
job = Job(glueContext)
job.init(job_name, args)
client = boto3.client('glue', region_name=region)



# Make this a global variable so it can't change if we run near midnight UTC
# Plus I'm not creating a new object for every record!
now = datetime.datetime.now()



def AddPartitions(rec):
    rec["yyyy"] = now.year
    rec["mm"] = now.month
    rec["day"] = now.day
    return rec


def transform(source_db, target_bucket, target_prefix, table_name, partition_keys = []):

    datasource0 = glueContext.create_dynamic_frame.from_catalog(database=source_db,
                                                                table_name=table_name,
                                                                transformation_ctx=table_name+"datasource0")



    map1 = Map.apply(frame=datasource0, f=AddPartitions, transformation_ctx=table_name+"map1")

    datasink1 = glueContext.write_dynamic_frame.from_options(
        frame=map1,
        connection_type="s3",
        connection_options={
            "path": "s3://" + target_bucket + "/" + target_prefix + "/" + table_name + "/",
            "partitionKeys": ["yyyy", "mm", "day"] + partition_keys},
        format="parquet"
    )


try:
    print('\nSource database name: ' + source_db)
    tables = client.get_tables(DatabaseName=source_db)
    for table in tables['TableList']:
        if 'DEPRECATED_BY_CRAWLER' not in table['Parameters']:
            table_name = table['Name']
            print('\n-- tableName: ' + table_name)
            partitions = table['PartitionKeys']
            if partitions is not []:
                # get partition keys
                partition_keys = []
                [partition_keys.append(partition['Name']) for partition in partitions]
                transform(source_db, target_bucket, target_prefix, table_name, partition_keys)
            else:
                transform(source_db, target_bucket, target_prefix, table_name)

except Exception as e:
    print(e)

job.commit()
