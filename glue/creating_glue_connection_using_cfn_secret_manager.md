One cannot use Secure Strings from SSM in defining Glue connections with CloudFormation.  As of today glue is not a supported resource that support dynamic parameter patterns for secure strings with CloudFormation. The list of resources that supports it is provided here - 

  https://docs.amazonaws.cn/en_us/AWSCloudFormation/latest/UserGuide/dynamic-references.html

Under the section "Resources that support dynamic parameter patterns for secure strings".

===============
Recommendation
===============

    As a workaround you can still use AWS Secrets Manager which can be used to obtain secrets for CloudFormation templates. 

    I had tested this approach with postgres RDS instance , it worked perfectly fine. Below is the YAML template that I used to create a brand new AWS glue connection that extracted the password for the postgres using AWS secret manager dynamically. This is something which can be used as an alternative until we rollout the feature for using SSM with Glue.

    As a step 1 you need to create a new secret in AWS secret manager , once done you can use this in the CFN template as below : 

    Default: '{{resolve:secretsmanager:rdspwd:SecretString:password}}'

    In the above syntax "rdspwd" is the parameter defined in the parameter store in SSM.Hence you can refer a parameter defined in SSM's parameter store with the secretsmanager as above.



---
AWSTemplateFormatVersion: '2010-09-09'
# Sample CFN YAML to demonstrate creating a connection
#
# Parameters section contains names that are substituted in the Resources section
# These parameters are the names the resources created in the Data Catalog
Parameters:
# The name of the connection to be created
  CFNConnectionName:
    Type: String
    Default: newishan
  CFNJDBCString:
    Type: String
    Default: "jdbc:postgresql://postgres.xxx.us-west-2.rds.amazonaws.com:5432/test"
  CFNJDBCUser:
    Type: String
    Default: "postgres"
  CFNJDBCPassword:
    Type: String
    Default: '{{resolve:secretsmanager:rdspwd:SecretString:password}}'
    NoEcho: true
#
# Resources section defines metadata for the Data Catalog
Resources:
   CFNConnectionMySQL:
    Type: AWS::Glue::Connection
    Properties:
      CatalogId: !Ref AWS::AccountId
      ConnectionInput:
        Description: "Connect to MySQL database."
        ConnectionType: "JDBC"
        #MatchCriteria: none
        PhysicalConnectionRequirements:
          AvailabilityZone: "us-west-2d"
          SecurityGroupIdList:
           - "sg-xxx"
          SubnetId: "subnet-xxxx"
        ConnectionProperties: {
          "JDBC_CONNECTION_URL": !Ref CFNJDBCString,
          "USERNAME": !Ref CFNJDBCUser,
          "PASSWORD": !Ref CFNJDBCPassword
        }
        Name: !Ref CFNConnectionName
