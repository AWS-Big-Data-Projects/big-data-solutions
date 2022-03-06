Issue 1:

Failure of task level rename/move operations that happens in the OutputCommit phase while writing parquet data in S3. These errors usually occur due to S3 eventual consistency model.

Reason for the above error:

When we perform write operation from Spark, Spark uses a OutputCommitter class to perform these writes. Since Spark operates in a distributed environment, the writes will be done by multiple executors and there will be multiple checks and balances in place to ensure the data has been "committed" to the target location. Spark handles the OutputCommit phase have 2 operation - commitTask and commitJob. In both these operations, 'rename' operation is executed. In HDFS, this is a simple rename operation. However, on s3 since there is no built-in 'rename' operation, COPY+DELETE operation is done to mimic the rename operation.

Issue 2:

Creation on an additional sub-folder under a partition is also caused due to s3 inconsistency issue.

Reason for the above error:

The issue seems to happening intermittently because of S3 eventual consistency. Copying of output files written from staging directory to the partition directory is a rename operation. This is triggered immediately after the actual partition directory (i.e supposed to be overwritten) is deleted. Once in a while, the partition directory even though is successfully deleted, at the time of rename EmrFS still sees the deleted directory and hits a bug because of which it ends up creating a sub directory under the partition directory.

Workaround:

While EMRFS bug does need to be fixed, but the reason this bug even came up is because of S3 consistency. Thus use of EMRFS consistent view should help with this bug not being hit. So that can be one recommendation to the customer

To use EMRFS consistent view in GLue ETL jobs. We need to set the job parameters as below:

Here is a trick how to pass "--conf" values to a job:

    Key: --conf
    Value: spark.hadoop.fs.s3.consistent=true


*****Important***** If we set Value: fs.s3.consistent=true we get below error in cloudwatch log events of a glue job:

Warning: Ignoring non-spark config property: fs.s3.consistent.metadata.autoCreate=true
Warning: Ignoring non-spark config property: fs.s3.consistent=true

Please note, this issue is faced when using glue version 0.9,1.0. So we need to set the above parameter for both 0.9 and 1.0 glue versions.


This error is being caused by s3 eventual consistency issues. When spark tries to commit the task output (copy the file from output/_temporary/ prefix to output/) its not able to find the file in the output/_temporary/ prefix.

There are 2 options to work around this issue:

1. Use glueVersion 1.0 (spark 2.4.3) - This version uses EMRFS which has the s3 optimized committer enabled by default(https://aws.amazon.com/blogs/big-data/improve-apache-spark-write-performance-on-apache-parquet-formats-with-the-emrfs-s3-optimized-committer/). This committer algorithm doesn't have the eventual consistency issues during task commits

2. Use EMRFS consistent view in glueVersion 0.9 - This can be enabled by setting the following conf in job arguments: --conf fs.s3.consistent=true. Please note that this will create a dynamodb table in the customers account and this can incur additional costs to the customer. (More information here: https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-plan-consistent-view.html)
