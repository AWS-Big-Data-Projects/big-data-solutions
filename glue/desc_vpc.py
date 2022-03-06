import boto3
client = boto3.client('ec2',region_name='us-west-2')
vpc_info=client.describe_vpcs()
print(vpc_info)
