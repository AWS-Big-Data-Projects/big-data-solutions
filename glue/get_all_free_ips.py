# Collect available IP adressses for subnets

import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    sns = boto3.client('sns')

    result = ec2.describe_subnets( Filters=[{'Name': 'state', 'Values': ['available']}])

    notify_message = """
    """
    for subnet in result['Subnets']:
        m = "Available IP's in subnet %s is %d" % (subnet['SubnetId'], subnet['AvailableIpAddressCount'])
        print m
        notify_message = notify_message+"\n"+m

    topicArn = 'arn:aws:sns:my_sns_topic'

    sns.publish(
        TopicArn = topicArn,
        Message = notify_message

   )
