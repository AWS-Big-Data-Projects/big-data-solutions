If you are trying to connect to Glue catalog from EMR by adding the following in /etc/spark/conf/hive-site.xml 

<property>
    <name>hive.metastore.client.factory.class</name>
    <value>com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory</value>
  </property>

After that, when you start spark-sql from the EMR master node, it hangs and fails with the following error

Caused by: org.apache.http.conn.ConnectTimeoutException: Connect to glue.us-west-2.amazonaws.com:443 [glue.us-west-2.amazonaws.com/52.34.21.56, glue.us-west-2.amazonaws.com/54.244.180.174, glue.us-west-2.amazonaws.com/52.38.63.163, glue.us-west-2.amazonaws.com/52.27.227.131] failed: connect timed out

This happens because the EMR cluster is not able to reach the regional endpoints for AWS Glue.

============================
Resolution Steps to Follow 
=============================

- Check the security groups for master and Slave nodes and see if outbound traffic to port 443 is restricted and allow traffic to 443 if the traffic is restricted.
- Check NACLs in VPC settings and make sure 443 egress and ephemeral port traffic for ingress is allowed - Refer https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html#nacl-ephemeral-ports.
- If the cluster is launched in a private subnet, please make sure there is a NAT gateway attached (for the cluster to communicate with glue using public endpoints/IPs) or a VPC Interface Endpoint (for the cluster to communicate with Glue using private endpoints/IPs) for AWS Glue is created in the VPC where the cluster is located - Please refer https://docs.aws.amazon.com/glue/latest/dg/vpc-endpoint.html. 

You can check the connectivity using Telnet to reach the regional endpoint. 

======
[hadoop@ip-xx-0-xx-xx ~]$ telnet glue.us-west-2.amazonaws.com 443
======

Once you're able to connect to the endpoint from Telnet, you can try using spark-sql again.  
