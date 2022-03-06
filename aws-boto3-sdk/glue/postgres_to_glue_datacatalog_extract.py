/**

1> launched a Postgres sever and created the table using following query:
  
CREATE TABLE ishan ("userID" VARCHAR (50) PRIMARY KEY, "UserName" VARCHAR (50));

2> Ran crawler on the Postgres sever which will create the table.

3> Create Glue ETL job by select source table as Postgres table "ishan" and target source as S3 location.

4> creata a glue pyspark job with the following code: 

**/

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import SQLContext
## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
spark.sql('set spark.sql.caseSensitive=true')
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
sqlContext = SQLContext(sc)
sqlContext.setConf("spark.sql.caseSensitive","true")


datasource0 = sqlContext.read.format("jdbc").option("url", "jdbc:postgresql://<postgres endpoint>:5432/postgres").option("query","select * from ishan").option("user", "postgres").option("password", "password").load()
datasource12=datasource0.repartition(1)                       
datasource1=DynamicFrame.fromDF(datasource12,glueContext,"test")
datasink2 = glueContext.write_dynamic_frame.from_options(frame = datasource1, connection_type = "s3", connection_options = {"path": "s3://<bucket-name>/images/"}, format = "csv", transformation_ctx = "datasink2")
job.commit()
