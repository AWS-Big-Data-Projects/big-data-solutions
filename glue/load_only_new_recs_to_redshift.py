#
#Script to load CSV files from S3 into a Redshift database using AWS Glue
#
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['TempDir', 'JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Continuous logging is required in the job definition for this logging
logger = glueContext.get_logger()

# Source and destination paths
glue_db = "productsetl"
glue_table_products = "productscsv"
glue_table_categories = "categoriescsv"
rs_db = "salesdw"
rs_table = "products"
s3_error_path = "s3://productscsvforetl/Errors"

# Load products file
productsDF = glueContext.create_dynamic_frame.from_catalog(
    database = glue_db, 
    table_name = glue_table_products, 
    transformation_ctx = "datasource0")
logger.info("Products count: " + str(productsDF.count()))

# Load categories file
categoriesDF = glueContext.create_dynamic_frame.from_catalog(
    database = glue_db, 
    table_name = glue_table_categories)
logger.info("Categories count: " + str(categoriesDF.count()))

# Remove deleted products
productsDF = productsDF.filter(f = lambda x: x["deleted"] == "N", transformation_ctx = "trans0")

# Convert launchdate string to date type and drop "deleted" column by not mapping it
productsDF = productsDF.apply_mapping(mappings = [
    ("id","bigint","id","bigint"),
    ("name","string","name","string"),
    ("category","bigint","category","bigint"),
    ("launchdate", "string", "launchdate", "date")],
    transformation_ctx = "trans1")

# Log null dates (i.e. null to begin with or failed conversion above) to an error data frame
errorDF = productsDF.filter(f = lambda x: x["launchdate"] is None, transformation_ctx = "trans2")

# Rename duplicate column names across both tables, join them, drop redundant fields
productsDF = productsDF.rename_field("name", "productname", transformation_ctx = "trans3")
categoriesDF = categoriesDF.rename_field("name", "categoryname").rename_field("id", "categoryid")
productsDF = productsDF.join(
    paths1 = ["category"], 
    paths2 = ["categoryid"], 
    frame2 = categoriesDF, 
    transformation_ctx = "trans4")
productsDF = productsDF.drop_fields(["category", "categoryid"], transformation_ctx = "trans5")

# Write products frame to Redshift
productsDF = glueContext.write_dynamic_frame.from_jdbc_conf(
    frame = productsDF, 
    catalog_connection = "Redshift SalesDW", 
    connection_options = {"dbtable": rs_table, "database": rs_db}, 
    redshift_tmp_dir = args["TempDir"],
    transformation_ctx = "datasink0")

# Write error frame to S3
if errorDF.count() > 0:
    errorDF = glueContext.write_dynamic_frame.from_options(
        frame = errorDF,
        connection_type = "s3", 
        connection_options = {"path": s3_error_path},
        format = "csv")

job.commit()
