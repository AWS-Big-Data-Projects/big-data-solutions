1. In my AWS Account A ( us-west-2 ) region : Wrote the below python script and created GlueETL Spark Job : 

          import boto3
          sqs = boto3.client('sqs')
        
          queue_url = 'https://sqs.us-east-1.amazonaws.com/AAAAA/glue-queue'
          response = sqs.send_message(
              QueueUrl=queue_url,
              DelaySeconds=10,
              MessageAttributes={
                  'Title': {
                      'DataType': 'String',
                      'StringValue': 'The Whistler'
                  },
                  'Author': {
                      'DataType': 'String',
                      'StringValue': 'John Grisham'
                  },
                  'WeeksOn': {
                      'DataType': 'Number',
                      'StringValue': '6'
                  }
              },
              MessageBody=(
                  'Information about current NY Times fiction bestseller for '
                  'week of 12/11/2016.'
              )
          )

          print(response['MessageId'])

    2. Provided SNS SendMessage permission to the IAM role what my GlueETL Spark Job job is using in account A with the other required permissions ( Default glue service role ): 

                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "VisualEditor0",
                            "Effect": "Allow",
                            "Action": "sqs:SendMessage",
                            "Resource": "*"
                        }
                    ]
                }

    3. In Account B - Created SQS queue with the below access policy :

              {
                "Version": "2008-10-17",
                "Id": "__default_policy_ID",
                "Statement": [
                  {
                    "Sid": "__owner_statement",
                    "Effect": "Allow",
                    "Principal": {
                      "AWS": "arn:aws:iam::BBBBBBB:root"
                    },
                    "Action": "sqs:SendMessage",
                    "Resource": "arn:aws:sqs:us-east-1:AAAAAA:glue-queue"
                  }
                ]
              }

    4. Ran the Glue job in Account A , it will fail with the error message i.e. 

          botocore.errorfactory.QueueDoesNotExist: An error occurred (AWS.SimpleQueueService.NonExistentQueue) when calling the SendMessage operation: The specified queue does not exist or you do not have access to it.
          
          
========================
Fix to run the GlueETL
========================

5. Made the change in the above Python script to include the region , since its a cross account and cross region request (i.e. Glue Job in Account A is running in us-west-2 but the SQS queue is present in us-east-1 and a differet AWS account ). 

I found within GlueETL while setting up the SQL client the region must be passed while sending message to SQS queue.This is especially true when the queue is in a different region.Otherwise it uses the same region where the client is set-up and running. 

    Changed Code => sqs = boto3.client('sqs',region_name="us-east-1")

Then I ran the GlueETL job with the updated code as above and included region , the job did SUCCEED without any issues.I verified the SQS queue by polling the message sent from the GlueETL job.
