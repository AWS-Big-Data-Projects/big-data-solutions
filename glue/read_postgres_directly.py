from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

datasource0 = glueContext.create_dynamic_frame.from_options(connection_type=“Postgres”, connection_options={"url": "<jdbc-string>/<db-name>", "user": "<username>", "password": "<password>","dbtable": "<view>"})
datasink2 = glueContext.write_dynamic_frame.from_options(frame = datasource0, connection_type = "s3", connection_options = {"path": "s3://<bucketname>/postgres-matview/"}, format = "json", transformation_ctx = "datasink2")
job.commit()

#Registering it as a temporary View within Spark

memberships.toDF().createOrReplaceTempView("memberships")
spark.sql("select distinct organization_id from memberships").show()

+--------------------+
|     organization_id|
+--------------------+
|d56acebe-8fdc-47b...|
|8fa6c3d2-71dc-478...|
+--------------------+
