import boto3
import gzip
import pandas as pd
import csv
from io import BytesIO, TextIOWrapper, StringIO

s3_client = boto3.client('s3')
s3_client.download_file('xxx', 'glue_internal_ser_error/cur-hourly-01.csv.gz', '/tmp/cur-hourly-01.csv.gz')

with gzip.open('/tmp/cur-hourly-01.csv.gz', 'rt') as f:
     file_content = f.readlines()
     print(file_content[:100])
