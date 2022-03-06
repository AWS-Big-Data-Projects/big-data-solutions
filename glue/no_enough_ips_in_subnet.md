This error happens when there aren't enough IP addresses available for the AWS Glue job. Here are two common reasons why this might happen:

    When you run a job in a Virtual Private Cloud (VPC) subnet, AWS Glue sets up elastic network interfaces that enable your job to connect securely to other resources in the VPC. Each elastic network interface gets a private IP address. If the elastic network interfaces aren't released in a timely manner, there might not be enough IP addresses available for the job. To resolve the error, confirm how many DPUs that the job used. Then, reduce the number of DPUs and run the job again. Or, delete unused elastic network interfaces.
    Multiple AWS services are using the same subnet. These services might be using many of the subnet's available IP addresses. To resolve the error, use a different subnet with more available IP addresses for the AWS Glue job.

============
Resolution
============

Use one of the following methods to resolve the error.

## Option 1 : Reduce the number of DPUs for the job

    After the job run completes, check how many DPUs that the job used:

        1. Open the AWS Glue console.
        2. On the navigation pane, choose Jobs.
        3. Choose the job, and then choose the History tab. The Maximum capacity column shows the number of DPUs used for the job.

    Reduce the number of DPUs for the job:

        1. Decide how many DPUs to remove from the job. Keep in mind that the number of DPUs doesn't equal the number of elastic network interfaces. One elastic network interface is always attached to each worker. However, additional elastic network interfaces are also required for each job:
        Standard worker type (1 DPU per worker): one additional elastic network interface required
        G1.X worker type (1 DPU per worker): two additional elastic network interfaces required
        G2.X worker type (2 DPUs): two additional elastic network interfaces required
        2. On the navigation pane, choose Jobs.
        3. Choose the Action dropdown menu, and then choose Edit job.
        4. Expand the Security configuration, script libraries, and job parameters (optional) list.
        5. In the Maximum capacity field, enter a lower number. This field sets the maximum number of DPUs that the job can use.
        6. Save your changes, and then run the job again.

## Option 2 : Delete unused elastic network interfaces

    For more information, see Deleting a network interface.[1]

## Option 3 :  Use a subnet that has more available IP addresses

    Create a new subnet:

        1. Create a new subnet in your VPC.[2]
        Note: You can create a new subnet using the VPC's original CIDR blocks, or add additional CIDR blocks[3] to your VPC to use with the new subnet.
        2. Review the route tables and access control list (ACL) rules associated with the old subnet to be sure that the new subnet routes traffic the same way. For example, if your previous subnet had a default route configured to an internet gateway, then be sure that your new subnet has a similar default route.

    Modify the AWS Glue connection to use the new subnet:

        1. Open the AWS Glue console.
        2. In the navigation pane, choose Connections.
        3. Select the check box next to the connection that the AWS Glue job is using.
        4. In the Action dropdown list, choose Edit connection.
        5. On the Set up your connection’s properties page, choose Next.
        6. On the Set up access to your data store page, in the Subnet dropdown list, choose the new subnet.
        7. Choose Next, and then choose Finish.
        8. Run the job again.

    To check the number of available IP addresses in the subnet:

        1. Open the AWS Glue console.
        2. In the navigation pane, choose Connections.
        3. Select the check box next to the connection that the AWS Glue job is using.
        4. In the Action drop-down list, choose View details. Note the subnet.
        5. Open the Amazon VPC console.
        6. In the navigation pane, choose Subnets.
        7. In the Subnet dropdown list, choose the subnet that the AWS Glue connection is using.
        8. On the Description tab, check the Available IPv4 Addresses field. This field shows how many IP addresses are available in the subnet.

        References :

      [1]https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#delete_eni
      [2] https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#AddaSubnet
      [3] https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#vpc-resize
