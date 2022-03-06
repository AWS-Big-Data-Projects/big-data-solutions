
=================
Recommendations
=================


There are multiple ways to narrow down the problem and see what is causing this behavior : 


1. Look at the Spark UI and understand where is the bottleneck .Please try to understand where exactly the PySpark code is taking too much of time and this can be only determined by looking at the sparkUI while the application is running .  I had included couple of URLs you can take a quick look to understand what to look for while doing a deep dive into Spark UI while the application is running ? [1] to [4]

2. Try to configure app with these configurations which can be passed along with spark-submit using  --conf  or setting inside the python code itself. 

Example : spark-submit --master yarn --deploy-mode cluster --executor-memory 4g --driver-memory 4g --conf spark.executor.memoryOverhead=512 demo.py

          Further, let’s assume that we do this through an Amazon EMR cluster with 1 m4.4xlarge master node and 20 m4.4xlarge core nodes. Each m4.4xlarge instance has 16 virtual cores (vCPUs) and 64 GB RAM. All these calculations are for the --deploy-mode cluster, which we recommend for production use.


          vCPU=16
          Mem=64

          =================================================================================


          ====
          spark.executor.cores=5
          ====

          Number of executors per instance = (total number of virtual cores per instance - 1)/ spark.executors.cores

          Number of executors per instance = (16- 1)/ 5 = 15 / 5 = 3 (rounded down)

          Total executor memory = total RAM per instance / number of executors per instance

          Total executor memory = 64/3 = 21

          spark.executors.memory = total executor memory * 0.90
          spark.executors.memory = 21 * 0.90 = 18 (rounded down)

          spark.yarn.executor.memoryOverhead = total executor memory * 0.10
          spark.yarn.executor.memoryOverhead = 21 * 0.1 = 2 (rounded up)

          ==
          spark.executor.memory = 18
          ===


          ====
          spark.driver.memory = spark.executors.memory = 18 G
          ====

          ===
          spark.driver.cores = spark.executor.cores
          spark.driver.cores = 5
          ===

          ===
          number of core instances = No of core nodes in the cluster = 20 
          spark.executor.instances = (number of executors per instance * number of core instances) minus 1 for the driver

          spark.executor.instances = 3 * 20 -1 = 59

          ====

          ===
          spark.default.parallelism = spark.executor.instances * spark.executors.cores * 2

          spark.default.parallelism = 59 * 5 * 2 = 590

          Warning: Although this calculation gives partitions of 590, we recommend that you estimate the size of each partition and adjust this number accordingly by using coalesce or repartition.

          In case of dataframes, configure the parameter spark.sql.shuffle.partitions along with spark.default.parallelism.

          set the virtual and physical memory check flag to false.

          "yarn.nodemanager.vmem-check-enabled":"false",
          "yarn.nodemanager.pmem-check-enabled":"false"

          ====


4. Using EMRFS s3-optimized committer - The EMRFS S3-optimized committer is an alternative OutputCommitter implementation that is optimized for writing files to Amazon S3 when using EMRFS. But the committer is available with Amazon EMR release version 5.19.0 and later, and is enabled by default with Amazon EMR 5.20.0 and later.Hence you need to use EMR release version 5.19.0 or later to take benefit of it.

5. Enabling SparkUI on AWS EMR  - 

        The web interfaces in EMR are hosted on various ports on localhost and are enabled by default. To access these Web UI on your local machine, you can establish an SSH tunnel with dynamic ports. However, If EMR cluster is hosted in a VPC, therefore, establishing a direct tunnel in this case will not be possible since the cluster's master node does not have a public IP.

        A work around for this would be to create a bastion host in your VPC under a public subnet and establishing a tunnel to that. The bastion host can then help us establish a connection to the EMR cluster's master node.

        ====== Create and Configure Bastion Host ==============================================================

        1) Launch a bastion host( an EC2 instance with a public subnet ) and make sure that the bastion and the EMR are in the same VPC.

        2) Check if the bastion can access the EMR Master node. To do this, SSH into the bastion from your local machine, and then, from the bastion try to SSH into the master node of the cluster(using the EMR clusters internal IP).

        3) Next, we establish a tunnel. To do this, please execute the following on your local machine:
                ssh -i key_name.pem ec2-user@Public IP(Bastion Host)  -ND 8157

        The above command establishes a dynamic port (-D) to your bastion from your local machine.
        ====== Enable Proxies ==============================================================================

        Note: If you already have proxies enabled(foxy proxy), please ignore this section and continue reading

        1) On your web browser (I used firefox and it worked like a charm!), download the foxy proxy extension [6], and make sure "Use Enabled Proxies By Patterns and Priority" option is selected.
         
        2) I am attaching my foxy proxy config which you can import. To do this, follow the below:

            FoxyProxy options > Import > Under "Import Settings from FoxyProxy 6.x (current version)", click Browse > Provide the file I have attached(foxyproxy.json) > 
            Accept any overwrite warnings. Make sure emr-socks-proxy is enabled as well after import is completed
                    
            Note: While establishing a tunnel, if you used a port different from 8157, then you will have to modify your foxyproxy settings to update the port number(FoxyProxy options > Edit emr-socks-proxy > Update Port > Save)
        You should now be able to view your web UI on your firefox using the below format:

            http://<EMR DNS>:<PORT>/
        The EMR DNS will look something like ip-10-xx-xx-xx.ec2.internal.

        Assuming you have some SparkContext active (eg ran 'pyspark'), you can access it on port 4040. Please note that for each spark application session, the port keeps on incrementing. It initially starts from port 4040.

        The Spark History Server can be access on port 18080. The Resource Manager on port 8088. For a complete list of available ports, please look at the attached AWS documentation [7]




References :
[1] https://medium.com/analytics-vidhya/spark-ui-c7f2ca9ef97f
[2] https://databricks.com/blog/2015/06/22/understanding-your-spark-application-through-visualization.html
[3] https://www.protechtraining.com/blog/post/tuning-apache-spark-jobs-the-easy-way-web-ui-stage-detail-view-911
[4] https://sparkbyexamples.com/spark/spark-web-ui-understanding/
[5] https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark-s3-optimized-committer.html
[6] Foxy Proxy Extension for Firefox: https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/
[7] EMR Web Interfaces: https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-web-interfaces.html

