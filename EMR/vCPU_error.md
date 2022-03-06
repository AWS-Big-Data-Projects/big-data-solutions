"errorCode": "Client.VcpuLimitExceeded",

"errorMessage": "You have requested more vCPU capacity than your current vCPU limit of 1111 allows for the instance bucket that the specified instance type belongs to. Please visit http://aws.amazon.com/contact-us/ec2-request to request an adjustment to this limit.
    
This error indicates that one need to request for the limit increase for instance family type in order to provision on-demand instances. You can calculate the current EC2 limit for the R-type instance by "Calculate vCPU limit" .

EC2 vCPU limit increases are submitted as a vCPU value. To request an increase, Kindly determine how many vCPUs your On-Demand Instances are using. You can use the vCPU limits calculator to measure the number of vCPUs that you are currently using against vCPU-based limits to determine the appropriate service limit increase to request. 

You can create a service limit request directly from the vCPU limits calculator. 



Ref: https://aws.amazon.com/premiumsupport/knowledge-center/ec2-on-demand-instance-vcpu-increase/
