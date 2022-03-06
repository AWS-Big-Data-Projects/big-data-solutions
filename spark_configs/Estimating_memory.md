Estimating Memory and CPU utilization for Spark jobs :

Analytically calculating memory and CPU utilization for each Spark job is not a straightforward process. However, to estimate resources for troubleshooting purposes, the following methodology typically helps.

The following example illustrates the use of cores and executors in estimating resources for any job.

Let's consider an example for 5 node cluster with 80 cores and 320 GB memory.
Let us assume that for 1 node,  we estimate 16 cores and 64GB memory.

The math justifying the above estimates is as follows: 
1) Let's save 2 cores and 8 GB per machine for OS and stuff (Then you have 74 cores and 280 GB for Spark)
 
2) As a rule of thumb, use 3 - 5 threads per executor reading from MFS. Assume 3, then it is 3 cores per executor.

--executor-cores = 3


3) Per node we have 14 cores, to be on the safe side subtract 1 core for AM, divide it by cores per executor. Then the number of executors per node is (14 - 1) / 3 = 4.
We have 5 nodes, so:

--num-executors = 20


BTW. 3 cores * 4 executors mean that potentially 12 threads are trying to read from MFS per machine.
 
4) Per node we have 64 - 8 = 56 GB. Having from above 4 executors per node, this is 14 GB per executor.
Remove 10% as YARN overhead, leaving 12GB

--executor-memory = 12


This leads to 20*3 = 60 cores and 12 * 20 = 240 GB, which leaves some further room for the machines.
 
You can also start with 4 executor-cores, you'll then have 3 executors per node (num-executors = 15) and 19 GB of executor memory.
