Use case : If you have a glue "connection" failure in say us-west-2 region and you try to connect to the redshift/postgres etc. cluster running in different region say us-east-1.

	* when a glue connection is created using the VPC id (vpc-a) in us-west-2 region whereas the redshift cluster uses VPC id (vpc-b) in us-east-1. Since the resources are in different VPCs, one must enable VPC peering so that the glue jobs in us-west-2 can connect to the redshift cluster in us-east-1.

	* I would like to highlight that, VPC peering connection is a networking connection between two VPCs that enables you to route traffic between them using private IPv4 addresses or IPv6 addresses[1]. 

	* After creating the VPC peering connection[2], one must update the VPC subnets route tables to allow traffic from the accepted VPC CIDR. Please refer the documentation[3] for more details to configure route tables.

	* Update the redshift cluster security group to allow traffic from the us-west-2 VPC CIDR.

	* To test the connection, one can test EC2 instance using the same network properties(subnet & security group) used for glue connection and use the below telnet command to check the connectivity to redshift.

	$ sudo yum install telnet -y
	$ telnet <redshift_hostaname> <port_number>

	* Using telnet command one should be able to connect to the redshift cluster and then the glue "test connection" will work too.
  
  -References:
=============
[1] https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html
[2] https://docs.aws.amazon.com/vpc/latest/peering/create-vpc-peering-connection.html
[3] https://docs.aws.amazon.com/vpc/latest/peering/peering-configurations-full-access.html

