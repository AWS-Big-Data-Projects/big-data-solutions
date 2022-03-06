Just to ensure , as we understand there are only two ways to get Glue jobs with internet connectivity:

    I) Scenario 1 : No AWS Glue Connection attached. Jobs that are NOT attached to a Connection will get Internet connectivity out of the box.

    II) Scenario 2  :  If AWS Glue Connection is attached, then its associated subnet MUST include a route to a NAT Gateway (NAT GW). Public subnets (that is, subnets with a route to 0.0.0.0/0 via Internet Gateway or IGW) are useless for Glue because the Elastic Network Interfaces (ENIs) that the service creates for the jobs will ONLY have private IP addresses assigned. As you might now, for a private IP to be able to go out to the Internet, a network address translation (NAT) must take place in order to "map" the private IP to a public one. Only then the traffic can go out to the internet.Basically, this setup would be like the one mentioned here [1].


In the meantime, I would recommend you to review our Glue documentation titled "Setting Up Your Environment to Access Data Stores" [2], especially these paragraphs:

   """
   If a job needs to run in your VPC subnet—for example, transforming data from a JDBC data store in a private subnet—AWS Glue sets up elastic network interfaces that enable your jobs to connect securely to other resources within your VPC. Each elastic network interface is assigned a private IP address from the IP address range within the subnet you specified. No public IP addresses are assigned. Security groups specified in the AWS Glue connection are applied on each of the elastic network interfaces. For more information, see Setting Up a VPC to Connect to JDBC Data Stores.

   All JDBC data stores that are accessed by the job must be available from the VPC subnet. To access Amazon S3 from within your VPC, a VPC endpoint is required.
   If your job needs to access both VPC resources and the public internet, the VPC needs to have a Network Address Translation (NAT) gateway inside the VPC. 
   """

And then please verify that you Glue Connection's subnet has a route to a NAT Gateway so that your job can get internet connectivity as described above (i.e., "if your job needs to access both VPC resources and the public internet, the VPC needs to have a Network Address Translation -NAT- gateway inside the VPC")

Please verify all these steps mentioned above , if you still run into issues , please provide us with the glue connection details . You can take a snapshot of glue connection which is attached to the job providing all the networking details.

====== REFERENCES ======

[1] VPC with public and private subnets (NAT) - https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario2.html
[2] Setting Up Your Environment to Access Data Stores - https://docs.aws.amazon.com/glue/latest/dg/start-connecting.html
