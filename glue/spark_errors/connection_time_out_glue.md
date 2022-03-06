If Glue Job is failing to connect to the GlueData Catalog metastore and failing with the error message:

       Caused by: org.apache.http.conn.ConnectTimeoutException: Connect to glue.us-east-1.amazonaws.com:443
       
A setup is required to run your glue job which connects to JDBC data source and Glue DataCatalog within your own VPC subnet. 

====================================
Why this VPC setup is required ? 
====================================

    To enable AWS Glue components to communicate, you must set up access to your data stores, such as Amazon Redshift and Amazon RDS. Where as if the job  doesn't need to run in your virtual private cloud (VPC) subnet—for example, transforming data from Amazon S3 to Amazon S3—no additional configuration is needed. 

    AWS Glue obtains the VPC/subnet and security group parameters for ENIs from the selected JDBC connection configuration. AWS Glue then creates ENIs and accesses the JDBC data store over the network. This is required for an AWS Glue ETL job that is set up with a JDBC connection.AWS Glue creates elastic network interfaces in your subnet using private IP addresses. Spark jobs use these elastic network interfaces to access your data sources and data targets. Traffic in, out, and within the Spark environment is governed by your VPC and networking policies with one exception: Calls made to AWS Glue libraries can proxy traffic to AWS Glue API operations through the AWS Glue VPC. 
    
================================
Networking Configuration Changes 
=================================


VPC endpoint for the s3 service

==========================================
Why S3 VPC endpoints (VPCe)is  required ?
==========================================

 AWS Glue uses Amazon S3 to store ETL scripts and temporary files. S3 can also be a source and a target for the transformed data. Amazon S3 VPC endpoints (VPCe) provide access to S3, as described in Amazon VPC Endpoints for Amazon S3. Hence, to access Amazon S3 from within your virtual private cloud (VPC), an Amazon S3 VPC endpoint is required.More details can be found here on s3 VPC endpoints [3].
              
              
 =================================================
Why self-referencing inbound rule is required ? 
==================================================

  This is needed because By creating a self-referencing rule, you can restrict the source to the same security group in the VPC, and it's not open to all networks. To allow AWS Glue to communicate with its components, we must specify a security group with a self-referencing inbound rule for all TCP ports. This security group attaches to AWS Glue elastic network interfaces in a specified VPC/subnet. It enables unfettered communication between the ENIs within a VPC/subnet and prevents incoming network access from other, unspecified sources. More details can be found here [4].
            

=========================================================
Why subnet association is required with the route tables ?
=========================================================

Your VPC has an implicit router, and you use route tables to control where network traffic is directed. 

Each subnet in your VPC must be associated with a route table, which controls the routing for the subnet (subnet route table). You can explicitly associate a subnet with a particular route table. Otherwise, the subnet is implicitly associated with the main route table. A subnet can only be associated with one route table at a time, but you can associate multiple subnets with the same subnet route table.You can find more details here .[1] and [2]


====================================
Why did we setup Glue VPC endpoint ?
====================================

 If you use Amazon Virtual Private Cloud (Amazon VPC) to host your AWS resources, you can establish a private connection between your VPC and AWS Glue. You use this connection to enable AWS Glue to communicate with the resources in your VPC without going through the public internet.

 Amazon VPC is an AWS service that you can use to launch AWS resources in a virtual network that you define. With a VPC, you have control over your network settings, such the IP address range, subnets, route tables, and network gateways. To connect your VPC to AWS Glue, you define an interface VPC endpoint for AWS Glue. When you use a VPC interface endpoint, communication between your VPC and AWS Glue is conducted entirely and securely within the AWS network.

You can use AWS Glue with VPC endpoints in all AWS Regions that support both AWS Glue and Amazon VPC endpoints.        
       
       
       
       
 
References :
[1] https://docs.aws.amazon.com/vpc/latest/userguide/WorkWithRouteTables.html#AssociateSubnet
[2] https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html#route-table-assocation
[3] https://docs.aws.amazon.com/vpc/latest/userguide/vpc-endpoints-s3.html
[4] https://docs.aws.amazon.com/glue/latest/dg/setup-vpc-for-glue-access.html
      

       
       #Code to test glue data catalog connectivity within ETL script 
       
       import sys
        from awsglue.transforms import *
        from awsglue.utils import getResolvedOptions
        from pyspark.context import SparkContext
        from awsglue.context import GlueContext
        from awsglue.job import Job
        from awsglue.dynamicframe import DynamicFrame
        ## @params: [JOB_NAME]
        args = getResolvedOptions(sys.argv, ['JOB_NAME'])
        sc = SparkContext()
        glueContext = GlueContext(sc)
        spark = glueContext.spark_session
        job = Job(glueContext)
        job.init(args['JOB_NAME'], args)
        spark.sql("SHOW TABLES").show()
        spark.sql('show databases').show()
        spark.catalog.currentDatabase()
        spark.sql('show tables from default').show()
