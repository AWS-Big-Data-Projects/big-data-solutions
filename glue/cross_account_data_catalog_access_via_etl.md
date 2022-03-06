Cross Account Setup for Glue ETL Jobs to access AWS Glue Data Catalog Objects in a different AWS Account.

Step 1 : 

Add the below policy to the Glue data Catalog settings in the AWS account where the Glue DataCatalog exists .

{
	"Version": "2012-10-17",
	"Statement": [{
		"Effect": "Allow",
		"Principal": {
			"AWS": "arn:aws:iam::<aws-accountID-Where-ETL-Runs>:role/glue_full_access_for_s3"
		},
		"Action": "glue:*",
		"Resource": ["arn:aws:glue:us-west-2:<aws-accountID-Where-catalog-resides>:catalog",
			"arn:aws:glue:us-west-2:<aws-accountID-Where-catalog-resides>:database/default",
			"arn:aws:glue:us-west-2:<aws-accountID-Where-catalog-resides>:table/default/*",
			"arn:aws:glue:us-west-2:<aws-accountID-Where-catalog-resides>:database/global_temp"
		]
	}]
}

Note : In case you want to give access to everyone in aws-account-Where-ETL-Runs provide this as well in the above policy in Principal.Adding this will give access to all IAM users/roles in the account-Where-ETL-Runs.

    "AWS":"arn:aws:iam::<aws-accountID-Where-ETL-Runs>:root"










Step 2 : 

Provide the permission to the IAM User/Role in the aws-account-Where-ETL-Runs . This role must be attached to the Glue Job.

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "glue:GetDatabase",
                "glue:GetConnection",
                "glue:GetTable",
                "glue:GetPartition",
                "glue:GetPartitions"
            ],
            "Resource": [
                "arn:aws:glue:us-west-2:<aws-accountID-Where-catalog-resides>:catalog",
                "arn:aws:glue:us-west-2:<aws-accountID-Where-catalog-resides>:database/default",
                "arn:aws:glue:us-west-2:<aws-accountID-Where-catalog-resides>:table/default/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": [
                "*"
            ]
        }
    ]
}


Note : Refine the above policy per your requirement.









Step 3 : 

  If the GlueData catalog objects in aws-accountID-Where-catalog-resides points to the s3 - you must provide below policy to the relevant s3 bucket to which database is pointing to.


{
    "Version": "2012-10-17",
    "Id": "Policy1587912647278",
    "Statement": [
        {
            "Sid": "Stmt1587912633716",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::<aws-accountID-Where-ETL-Runs>:role/cross_account_glue_role",
                    "arn:aws:iam::<aws-accountID-Where-ETL-Runs>:root"
                ]
            },
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::<s3-bucket-where-catalog-database-is-pointing>",
                "arn:aws:s3:::<s3-bucket-where-catalog-database-is-pointing>/*"
            ]
        }
    ]
}

















Step  4 : 

Testing the ETL Job in the aws-account-Where-ETL-Runs.

Sample PySpark Code I :

    from pyspark.sql import SparkSession 

    spark_session = SparkSession.builder.appName("EMR Spark Glue Example").config("hive.metastore.client.factory.class", "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory").config("hive.metastore.glue.catalogid", ":<aws-accountID-Where-catalog-resides>").enableHiveSupport().getOrCreate()

    table_df = spark_session.sql("show databases")
    table_df.show()
    table_df = spark_session.sql("use default")
    data_df = spark_session.sql("select * from <table-name> limit 2")
    data_df.show()

Sample PySpark Code II:


import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

glueContext = GlueContext(spark)
spark = glueContext.spark_session

datasource0 = glueContext.create_dynamic_frame.from_catalog(database="default",table_name="review_parquet",catalog_id="":<aws-accountID-Where-catalog-resides>")

datasource0.printSchema()
new = datasource0.toDF()
new.show()
