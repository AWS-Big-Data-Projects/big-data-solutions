import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

##################
## Update these variables with your own information
##################
DB_NAME = "instacart"

TBL_RAW_PRODUCTS = "raw_products"
TBL_RAW_ORDERS = "raw_orders"
TBL_RAW_ORDERS_PRIOR = "raw_orders_prior"
TBL_RAW_DEPT = "raw_departments"

OUTPUT_S3_PATH = "s3://xxx/temp/instacart/"
##################

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

## Create Glue and Spark context variables
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

## Define the source tables from where to read data
products = glueContext.create_dynamic_frame.from_catalog(database = DB_NAME, table_name = TBL_RAW_PRODUCTS, transformation_ctx = "products").toDF()
orders = glueContext.create_dynamic_frame.from_catalog(database = DB_NAME, table_name = TBL_RAW_ORDERS, transformation_ctx = "orders").toDF()
orders_prior = glueContext.create_dynamic_frame.from_catalog(database = DB_NAME, table_name = TBL_RAW_ORDERS_PRIOR, transformation_ctx = "orders_prior").toDF()
departments = glueContext.create_dynamic_frame.from_catalog(database = DB_NAME, table_name = TBL_RAW_DEPT, transformation_ctx = "departments").toDF()

## Fix the products table which was missing columns and types
p_df = products.withColumn('product_id', products.col0.cast('bigint')) \
.withColumn('product_name', products.col1.cast('string')) \
.withColumn('aisle_id', products.col2.cast('bigint')) \
.withColumn('department_id', products.col2.cast('bigint')) \
.na.drop('any')
df = p_df.select('product_id', 'product_name', 'aisle_id', 'department_id')

## Drop records that contain any null values
orders = orders.na.drop('any')
orders_prior = orders_prior.na.drop('any')
departments = departments.na.drop('any')

## Join the prior orders table with the products table
priors_products = orders_prior.join(df, ['product_id'])

## Join the previously join table with the departments table
orders_prod_dept = priors_products.join(departments, ['department_id'])

## Write out the current orders table to S3 partitioned by order day of week
orders.orderBy('user_id').coalesce(10).write.partitionBy('order_dow').mode('overwrite').parquet(OUTPUT_S3_PATH + 'current_orders/')

## Write out the joined table partitioned by department name
orders_prod_dept.orderBy('order_id').coalesce(10).write.partitionBy('department').mode('overwrite').parquet(OUTPUT_S3_PATH + 'prior_orders/')

job.commit()
