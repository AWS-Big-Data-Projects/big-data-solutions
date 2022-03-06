import boto3
s3 = boto3.resource('s3')
copy_source = {
      'Bucket': 'aws-logs-456690477084-us-west-2',
      'Key': 'bookmark_test.py'
    }
bucket = s3.Bucket('aws-jupyterhubtest')
bucket.copy(copy_source, 'temp/bookmark_test.py')
