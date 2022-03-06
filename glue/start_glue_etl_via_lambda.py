#
#Function that starts a Glue job called ProductsETL and is invoked by 
#an object creation event on an S3 bucket called productscsvforetl 
#
import boto3

glue = boto3.client('glue')

def lambda_handler(event, context):
    glue.start_job_run(
        JobName = 'ProductsETL',
        Arguments = {
            '--glue_db' : 'productsetl',
            '--glue_table_products' : 'productscsv',
            '--glue_table_categories' : 'categoriescsv',
            '--redshift_db' : 'salesdw',
            '--redshift_table' : 'products',
            '--s3_error_path' : 's3://productscsvforetl/Errors'
        }                
    )

