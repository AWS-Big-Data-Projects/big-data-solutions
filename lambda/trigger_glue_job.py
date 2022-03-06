import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    print( "Ishan Glue Lambda")
    client = boto3.client('glue')
    client.start_job_run(JobName = 'MovieDataRawToRefine',Arguments = {} )
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
