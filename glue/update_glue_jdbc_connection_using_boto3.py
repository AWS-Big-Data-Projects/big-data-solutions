
# Please replace all the parameter value's as per your use case

from pprint import pprint
import boto3

client = boto3.client('glue')
response = client.update_connection(
    Name='testdb',
    ConnectionInput={
        'Name': 'testdb', # Replace with your database name
        'Description': 'created via boto3',
        'ConnectionType': 'JDBC',
        'ConnectionProperties': {
            'JDBC_CONNECTION_URL': 'jdbc:mysql://10.0.0.0:3306/dbname',  # Replace with your database URL
            'JDBC_ENFORCE_SSL': 'true',# This Parameter is responsible for checking if SSL is enabled or not
            'PASSWORD': 'pw',
            'USERNAME': 'un'
        },
        'PhysicalConnectionRequirements': {
            'SubnetId': '<your-subnet-id>', # Replace with your subnet ID
            'SecurityGroupIdList': [
                '<your-security-group>',# Replace with your security group
            ],
            'AvailabilityZone': '<your-availability-zone>' #Replace with your AvailabilityZone
        }
    }
)
pprint(response)
