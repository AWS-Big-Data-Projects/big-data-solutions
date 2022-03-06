import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
import boto3
import base64
from botocore.exceptions import ClientError
import json

def get_secret():

    secret_name = "prod/glue/athenaview"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            
    # Your code goes here
    return json.loads(get_secret_value_response['SecretString'])


secrets = get_secret()
db_username = sectrets['db_username']
db_password = sectrets['db_password']
db_url = sectrets['db_url']

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()

glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# tablename = "databasename.viewname"
table_name = "vpc1.viewtest"

# the Jar file AthenaJDBC42_2.0.7.jar has to be passed as Dependent Jars path in S3
jdbc_driver_name = "com.simba.athena.jdbc.Driver"

# S3OutputLocation can be found in settings section of Athena query editor console
S3OutputLocation = "s3://aws-athena-query-results-000000000000-eu-central-1/"
df = glueContext.read.format("jdbc").option("driver", jdbc_driver_name).option("url", db_url).option("S3OutputLocation",S3OutputLocation).option("dbtable", table_name).option("user", db_username).option("password", db_password).load()

df.printSchema()

# converting the Dataframe to Dynamicframe
datasource0 = DynamicFrame.fromDF(df, glueContext, "datasource0")

# use the dynamic frame for further processing
glueContext.write_dynamic_frame.from_options(frame = datasource0,
          connection_type = "s3",
          connection_options = {"path": "s3://outputbucket/parquet1"},
          format = "parquet")
job.commit()
