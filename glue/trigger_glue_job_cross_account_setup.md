Trigger a crawler in Account B account after successful completion of Glue job in other account A. You can achieve this using CloudWatch Events. In CloudWatch you can make use of Event Buses, which allow to you achieve your current use-case. Please refer to [1] for information on how to set this up. 

This will mainly allow you to trigger a lambda function using CloudWatch Event in Account B after successful completion of Glue ETL job in Account A. You can make use of Boto3 Glue API calls [2] to trigger a crawler within your lambda script. 

Steps -
1. Create a Glue Job in Account A

2. In Account B, select Event Buses in CloudWatch console, click on Add Permission, and enter the Account ID of Account A

3. Create a CloudWatch rule for the job in Account A as below - 

========
{
  "source": [
    "aws.glue"
  ],
  "detail-type": [
    "Glue Job State Change"
  ],
  "detail": {
    "jobName": [
      "YourJobName"
    ],
    "state": [
      "SUCCEEDED"
    ]
  }
}
=========

And add a target that will send events to the event bus in Account B. 

4. In Account B, create a Lambda function using Boto3 Glue API calls, which will start the crawler.

5. In Account B, create a similar rule as step 3, but for targets, select the Lambda function created in step 4.



References -
[1] Event Buses - https://aws.amazon.com/blogs/aws/new-cross-account-delivery-of-cloudwatch-events/
[2] Boto3 Glue API calls - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html
