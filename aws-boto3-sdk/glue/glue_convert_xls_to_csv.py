import sys
import xlrd
import boto3
import csv
import os
import os.path

def upload_file(file_name, bucket, object_name=None):

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

s3_client = boto3.client('s3')

# Download the file from S3
s3_client.download_file('<your-aws-s3-bucket>', '<excel-file-s3-path>', '<glue-local-excel-file-path>')

with xlrd.open_workbook('<glue-local-excel-file-path>') as wb:
    print("File read successfully")
    sh = wb.sheet_by_index(0)
    with open('<glue-local-csv-file-path>', 'w', newline="") as f:
        c = csv.writer(f)
        for r in range(sh.nrows):
            c.writerow(sh.row_values(r))
print("Program finished and now uploading file to s3 now")

upload_file('<glue-local-csv-file-path>','<your-aws-s3-bucket>','<csv-file-s3-path>')


print("Upload successful")
