import boto3
client = boto3.client('glue')

response = client.update_table(
    DatabaseName='default',
    TableInput={
        'Name': 'scott_null_issue_pyspark_300241152ec040eab67902c52473bd37',
    },
    SkipArchive=True
)
