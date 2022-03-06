



Scheduling queries is useful in many scenarios, such as running periodic reporting queries or loading new partitions on a regular interval. Here are some of the ways that you can schedule queries in Athena:

    Create an AWS Lambda function, using the SDK of your choice, to schedule the query. For more information about the programming languages that Lambda supports, see AWS Lambda FAQs. Then, create an Amazon CloudWatch Events rule to schedule the Lambda function. This is the method explained in the Resolution.
    If you're using Athena in an ETL pipeline, use AWS Step Functions to create the pipeline and schedule the query.
    On a Linux machine, use crontab to schedule the query.
    Use an AWS Glue Python shell job to run the Athena query using the Athena boto3 API. Then, define a schedule for the AWS Glue job.



To schedule an Athena query using a Lambda function and a CloudWatch Events rule:

1.    Create an AWS Identity and Access Management (IAM) service role for Lambda. Then, attach a policy that allows access to Athena, Amazon Simple Storage Service (Amazon S3), and Amazon CloudWatch Logs. For example, you can add AmazonAthenaFullAccess and CloudWatchLogsFullAccess to the role. AmazonAthenaFullAccess allows full access to Athena and includes basic permissions for Amazon S3. CloudWatchLogsFullAccess allows full access to CloudWatch Logs.

2.    Open the Lambda console.

3.    Choose Create function.

4.    Be sure that Author from scratch is selected, and then configure the following options:

For Name, enter a name for your function.
For Runtime, choose one of the Python options.
For Role, choose Use an existing role, and then choose the IAM role that you created in step 1.

5.    Choose Create function.

6.    Paste your code in the Function code section. The following example uses Python 3.7. Replace these values in the example:

default: the Athena database name
SELECT * FROM default.tb: the query that you want to schedule
s3://AWSDOC-EXAMPLE-BUCKET/: the S3 bucket for the query output

import time
import boto3

query = 'SELECT * FROM default.tb'
DATABASE = 'default'
output='s3://AWSDOC-EXAMPLE-BUCKET/'

def lambda_handler(event, context):
    query = "SELECT * FROM default.tb"
    client = boto3.client('athena')

    # Execution
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': DATABASE
        },
        ResultConfiguration={
            'OutputLocation': output,
        }
    )
    return response
    return

7.    In the top-right corner of the page, choose Save.

8.    Open the CloudWatch console.

9.    In the navigation pane, choose Rules, and then choose Create rule. For more information about creating a CloudWatch Event rule, see Step 2: Create a Rule.

10.   In the Event Source section, choose Schedule, and then enter a cron expression.

11.   In the Targets section on the right side of the page, choose Add target.

12.   In the drop-down list, choose Lambda function.

13.   In the Function drop-down list, choose the name of your Lambda function.

14.   In the lower-right corner of the page, choose Configure details.

15.   Enter a Name and Description for your CloudWatch Events rule, and then choose Create rule.

16.   Open the Lambda console, and then choose the function that you created previously.

17.   Choose Add trigger, and then select CloudWatch Events/EventBridge.

18.   In the Rule drop-down list, choose the CloudWatch Events rule that you just created.

19.   Choose Add.

If you're scheduling multiple queries, keep in mind that there are quotas for the number of calls to the Athena API per account. For more information, see Per Account API Call Quotas.
