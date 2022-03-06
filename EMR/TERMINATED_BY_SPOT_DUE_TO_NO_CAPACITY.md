Spot Instances are spare compute capacity in the AWS Cloud. Spot Instance capacity is interrupted when Amazon Elastic Compute Cloud (Amazon EC2) needs the capacity back. The no Spot capacity available error occurs when there isn't enough spare capacity to fulfill your Spot Instance or Spot Fleet request.

As capacity becomes available, Amazon EC2 fulfills requests in the following order:

   1. Reserved Instances
   2. On-Demand Instances
   3. Spot Instances

The Spot request continues to automatically make the launch request until capacity becomes available. When capacity becomes available, Amazon EC2 fulfills the Spot request.

When setting up your Spot Instances, keep the following best practices in mind to help limit capacity issues:

   1. Use a diverse set of instance types so that you aren't reliant on one, specific type. You can create an Amazon EC2 Auto Scaling group with a mix of On-Demand and Spot Instances so that you aren't completely reliant on capacity availability. You are already doing this . Probably changing the instance type to a different one(s) will help. [1]

   2. Use the capacity optimized allocation strategy within your Auto Scaling group. The capacity optimized strategy analyzes real-time capacity data in order to launch your Spot Instances into pools with the most available capacity. [2]

For a complete list of best practices for utilizing Spot Instances successfully, see Best practices for EC2 Spot.[3]

If you want to find the interrupted Spot Instances and it's associated reason, you can refer this document[4]. In case you still run into this problem , please let us know we can connect over the phone and troubleshoot the problem further.

References:

[1] https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-purchase-options.html
[2] https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-purchase-options.html#asg-spot-strategy
[3] https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-best-practices.html
[4] https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-request-status.html#get-spot-instance-request-status
