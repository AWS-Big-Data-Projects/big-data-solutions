import sys
import configparser

import boto3

from io import StringIO

from awsglue.utils import getResolvedOptions
args = getResolvedOptions(sys.argv, ['env'])

str = args['env']
list = str.split('/')
key = str.split("/")[2] + "/" + str.split("/")[3] + "/" + str.split("/")[4]

s3 = boto3.resource('s3')
#obj = s3.Object(list[2], key)
obj = s3.Object(bucket_name='configparser', key='xxx/configparser/config.ini')
buf = StringIO(obj.get()['Body'].read().decode('utf-8'))

config = ConfigParser.ConfigParser()
config.readfp(buf)
print(config.get('SectionOne', 'Status'))

