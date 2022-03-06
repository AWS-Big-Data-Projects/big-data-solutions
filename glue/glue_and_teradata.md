As we are aware, Teradata is not natively supported by AWS Glue. With that being said, it is still possible to connect to a Teradata database with use of a dummy connection.

I have outlined the steps you would need to take to connect to your Teradata On-Prem/Cloud database.

Step 1:

Create a Dummy JDBC connection. You will need create a dummy JDBC connection and provide the VPC and subnet configuration which has network connectivity to your On-Prem Teradata database. Please note the JDBC URL is not important and can be as follows: jdbc:mysql://xxx-cluster.cluster-xxx.us-east-1.rds.amazonaws.com:3306/dummy

The important configuration in this step is to provide the correct VPC, private subnet and security group settings. Please note the subnet cannot be a public subnet (subnet with route to IGW). 

AWS Glue creates elastic network interfaces (ENIs) in the VPC/private subnet. These network interfaces then provide network connectivity for AWS Glue through your VPC. 

I recommend to read through the AWS blog [1] to get more insights into the network architecture and examples of the network configuration to set this up. 

Step 2:

Create a Glue ETL Job and add the dummy connection to the job. You will also need to provide the S3 location of the JDBC Driver. 

The Teradata blog [2] outlines the steps to create a job and provides the driver required to connect to the database.

You can then provide the connection details within your script to connect to the database. The blog also provides code samples to connect to the Teradata database and should be edited as per your requirement.

Providing the connection string within the Glue ETL script allows Glue to create secondary ENI's in the VPC and subnet you have configured to connect to the database.


References:
[1] https://aws.amazon.com/blogs/big-data/how-to-access-and-analyze-on-premises-data-stores-using-aws-glue/
[2] https://www.teradata.com/Blogs/Teradata-and-AWS-Glue
[3] https://aws.amazon.com/blogs/big-data/use-aws-glue-to-run-etl-jobs-against-non-native-jdbc-data-sources/
[4] https://kontext.tech/column/spark/315/connect-to-teradata-in-pyspark-via-jdbc

