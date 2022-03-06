Here's the list of API calls your Crawler will need access to:

* s3:ListBucket: To list objects in your S3 path
* s3:GetObject: To read objects in your S3 path and understand their schema

* glue:GetDatabase: To create tables in the designated database
* glue:GetTable: To verify whether the table already exists or not
* glue:CreateTable: To create the resulting output table
* glue:UpdateTable: To update the resulting output table if necessary
* glue:CreatePartition: To create partitions in the resulting output table
* glue:UpdatePartition: To update partitions in the resulting output table if necessary

* logs:CreateLogGroup: To create the LogGroup where your Crawler's CloudWatch logs will be written to
* logs:CreateLogStream: To create a LogStream inside the LogGroup
* logs:PutLogEvents: To push log messages to the created LogGroup and LogStream
