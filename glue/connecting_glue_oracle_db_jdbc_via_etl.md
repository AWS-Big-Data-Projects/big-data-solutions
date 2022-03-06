1. In this example, we create a variable with all the connection settings necessary for creating a Glue DynamicFrame connection. This is a manual connection where you specify the driver. It connects directly to the database and doesn't read the table from the Datacatalog. Note that this method puts the credentials in the job as plain text, and is not recommended  for production, I'll supply details about secret manager further down : 


We directly read from the Oracle database table using dynamic frame from_option API.

connection_oracle18_options = {
	"url": "jdbc:oracle:thin://@database-1.cakctb9fjzru.us-east-1.rds.amazonaws.com:2484/ORCL",
	"dbtable": "test",
	"user": "Admin",
	"password": "Master12345",
	"customJdbcDriverS3Path": "s3://aws-glue-data-ram/driver/ojdbc8.jar",
	"customJdbcDriverClassName": "oracle.jdbc.OracleDriver"}

datasource0 = glueContext.create_dynamic_frame.from_options(connection_type="oracle",connection_options=connection_oracle18_options)

(As per:
https://aws.amazon.com/blogs/big-data/use-aws-glue-to-run-etl-jobs-against-non-native-jdbc-data-sources/
 https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-glue-context.html#aws-glue-api-crawler-pyspark-extensions-glue-context-create_dynamic_frame_from_options
https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect.html#aws-glue-programming-etl-connect-jdbc
https://www.cdata.com/kb/tech/db2-jdbc-aws-glue.rst)


2. The alternative method is to establish the connection from within the Glue Connection (as you are attempting. In this case, you need the Test Connection to pass, and to run a Crawler to discover the tables. Then your job can simply read the table "from_catalog". This is the same as when you create a Glue job with the default auto-generated code: 


datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "MyDB", table_name = "myOracleTable")

(As per: 
https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-glue-context.html#aws-glue-api-crawler-pyspark-extensions-glue-context-create_dynamic_frame_from_catalog
)


3. Here is an example of the Oracle JDBC URL:
jdbc:oracle:thin://@database-2.<databaseHostname>.us-east-1.rds.amazonaws.com:1521/ORCL 
jdbc:oracle:thin://@database-1.cakctb9fjzru.us-east-1.rds.amazonaws.com:2484/ORCL


4. And if you want keep your passwords safe, the best practice is to use AWS Secret Manager (and then call it into the job using Boto3 code), or by using the Glue Connection, and getting the credentials from there:
import boto3
from awsglue.context import GlueContext
from pyspark.context import SparkContext
def get_glue_connection_credentials(connection_name, client=boto3.client('glue', region_name=‘us-east-1')):
    response = client.get_connection(Name=connection_name)
    connection_properties = response['Connection']['ConnectionProperties']
    url = connection_properties['JDBC_CONNECTION_URL']
    url_list = url.split("/")
    credentials = {
        'host': url_list[-2][:-5],
        'port': int(url_list[-2][-4:]),
        'dbname': url_list[-1],
        'user': connection_properties['USERNAME'],
        'password': connection_properties['PASSWORD']
    }
    return credentials

if __name__ == "__main__":
    spark_context = SparkContext()
    glue_context = GlueContext(spark_context)
    get_glue_connection_credentials('xrd_refdata')

(As per:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html )



5.1.  And lastely, if you would like to establish the connection using standard Spark, you can do so. 
dataframe1 = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:oracle:thin:username/password@//hostname:portnumber/SID") \
    .option("dbtable", "hr.emp") \
    .option("user", "db_user_name") \
    .option("password", "password") \
    .option("driver", "oracle.jdbc.driver.OracleDriver") \
    .load()

5.2. And if desired, you could transform the dataframe to a Glue DynamicFrame using fromDF(). 
from awsglue.dynamicframe import DynamicFrame
dynamicframe0 = DynamicFrame.fromDF(dataframe1, glueContext, "dynamicframe0")

(As per: 
https://dzone.com/articles/read-data-from-oracle-database-with-apache-spark
https://www.cdata.com/kb/tech/db2-jdbc-apache-spark.rst
https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-glue-context.html?shortFooter=true#aws-glue-api-crawler-pyspark-extensions-glue-context-write_dynamic_frame_from_catalog)

