To discover discrepancies between EMRFS metadata & Amazon S3 and make sure we have the EMRFS metadata in the DynamoDB in synchronized with the actual files on the S3 path.In order to do this, please follow the steps.

You need ssh into your Master node of your EMR cluster [Connect to the Master Node Using SSH https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-connect-master-node-ssh.html]

ssh -i youremr.pem hadoop@ipaddress.compute-1.amazonaws.com

Step 1: Run EMRFS diff to list the difference between your S3 path and the DynamoDB table --> Check for any differences 

Example: $ emrfs diff s3://elasticmapreduce/samples/cloudfront

Sample provided here https://docs.aws.amazon.com/emr/latest/ManagementGuide/emrfs-cli-reference.html#emrfs-diff

Step 2: Run EMRFS sync command to synchronize the dynamoDB table with the actual files in the S3 path

Example :emrfs sync s3://elasticmapreduce/samples/cloudfront

Step 3: Running EMRFS difff again shouldn't show you any difference with the DynamoDB & S3 path. If you dont find any differences , please try re-running the query again. If you still see a difference. then follow the Step 4.

Step 4: Run emrfs delete "emrfs delete s3://yourS3path" and then run Step 2 and Step 3 to ensure that there is no difference and then run your query.
