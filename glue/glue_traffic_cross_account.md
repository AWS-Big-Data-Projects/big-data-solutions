Creating cross account access for glue connection

1. Create VPC with public and private subnets in the account containing the Glue job.
2. Create a NAT gateway in the public subnet.
3. Create a route table for the private subnet including a route to "0.0.0.0/0" through the NAT gateway created in step 2.
4. Update inbound rule attached to Redshift cluster security group to allow traffic through NAT gateway.
5. Create Glue connection with the private subnet selected.
6. Edit the Glue job and select the connection created in step 5.
7. Run the Glue job.
