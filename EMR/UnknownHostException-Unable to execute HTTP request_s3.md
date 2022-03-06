1. To understand the issue better, Check if the issue was intermittent while trying to connection to S3 via EMR ? Are you able to reproduce this issue?

  2. Normally these errors are caused due to DNS issues, please run the following commands.

        1.1) dig <s3 end point> +short
        1.2) telnet <s3 end point> 443
        1.3) cat /etc/resolv.conf

          If the "dig" command returns an error then you will need to investigate your DNS server settings and the VPC if applicable The DNS settings may be misconfigured or the DNS server you are using is not operational. You may also need to implement DNS caching[1]. To troubleshoot the VPC I would suggest using the VPC flow logs[2].

  3. Check the s3 request-ids.

  4. Running a packet capture tcpdump/wireshark[4][5] and waiting for the fault to resurface.

  5. Monitoring the VPC[6] 

  6. Create a VPC endpoint for you s3 bucket, this will improve the performance to your s3 bucket as the data will go over the VPC endpoint[7][8]. VPC endpoints are normally implemented for security however it is recommended to use them which increases performance to a s3 bucket from your VPC.
  
  7. Lastly, pull the logs from the instance running the application, its found under - /var/log/message.
  


References:
[1]https://aws.amazon.com/premiumsupport/knowledge-center/dns-resolution-failures-ec2-linux/
[2]https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html
[3]https://docs.aws.amazon.com/Amazon/latest/userguide/get-request-ids.html
[4]https://www.tcpdump.org/
[5]https://www.wireshark.org/
[6] https://aws.amazon.com/blogs/networking-and-content-delivery/debugging-tool-for-network-connectivity-from-amazon-vpc/
[7] https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html
[8] https://aws.amazon.com/premiumsupport/knowledge-center/s3-private-connection-no-authentication/

