import pymongo
import sys
import boto3
from pyspark import SparkContext, SparkConf
conf = SparkConf().setAppName(appName).setMaster(master)
sc = SparkContext(conf=conf)

s3_client = boto3.client('s3')

# Download the file from S3
s3_client.download_file('xxx', 'docdb_cert/rds-combined-ca-bundle.pem', '/tmp/rds-combined-ca-bundle.pem')



## Create a MongoDB client, open a connection to Amazon DocumentDB as a replica set and specify the read preference as secondary preferred
client = pymongo.MongoClient('mongodb://ssl:xxx#@docdb-ssl-enabled.cluster-xx.us-west-2.docdb.amazonaws.com:27017/?ssl=true&ssl_ca_certs=rds-combined-ca-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false')

##Specify the database to be used
db = client.test

##Specify the collection to be used
col = db.ssl

##Insert a single document
col.insert_one({'hello':'Amazon DocumentDB'})

##Find the document that was previously written
x = col.find_one({'hello':'Amazon DocumentDB'})

##Print the result to the screen
print(x)

##Close the connection
client.close()
