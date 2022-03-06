import boto3
import os
from subprocess import call
import sys

### ===== Method 1: Read from the bash script file from the job environment =====
# # Functions to help locate the file.
# def _find(filename):
#     for dirname in sys.path:
#             candidate = os.path.join(dirname, filename)
#             if os.path.isfile(candidate): 
#                 return candidate
#     raise Error("Can't find file %s" % filename)

# def findFile(filename):
#     return _find(filename)

# # Locating the bash script `syncs3object.sh` in the Glue environment.
# bash_script_path = findFile("syncs3object.sh")
# with open(bash_script_path, 'rb') as file:
#     script = file.read()
### ===== End method 1. =====

### ===== Method 2: Read from S3 object directly. =====
# Initalize variables for the original S3 bucket source and the S3 bucket target destination.
source_s3_bucket = "original_source_bucket"
source_folder = "source_folder"
copy_target_path = "destination_target_bucket/target_folder"

# Assuming the bash script location is: `s3://MYBUCKET/MYFOLDER/syncs3object.sh`.
bash_script_s3_bucket_name = "MYBUCKET"
bash_script_s3_prefix_location = "MYFOLDER/syncs3object.sh"
script_contents = ""

# Read the bash script file from S3
s3 = boto3.client('s3')
result = s3.list_objects(Bucket=bash_script_s3_bucket_name, Prefix=bash_script_s3_prefix_location)
for o in result.get('Contents'):
    data = s3.get_object(Bucket=source_s3_bucket, Key=o.get('Key'))
    script_contents = data['Body'].read()
### ===== End method 2. =====

# Run the bash script to run `aws s3 sync s3://source-bucket/source-path s3://destination-bucket/destination-path`.
rc = call([script_contents, "", source_s3_bucket, source_folder, copy_target_path], shell=True)

print("Copied!")
