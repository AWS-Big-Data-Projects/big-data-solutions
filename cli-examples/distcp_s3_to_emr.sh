

https://aws.amazon.com/blogs/big-data/seven-tips-for-using-s3distcp-on-amazon-emr-to-move-data-efficiently-between-hdfs-and-amazon-s3/#6

Hadoop is optimized for reading a fewer number of large files rather than many small files, whether from S3 or HDFS. You can use S3DistCp to aggregate small files into fewer large files of a size that you choose, which can optimize your analysis for both performance and cost.

$ s3-dist-cp --src /data/incoming/hourly_table --dest s3://my-tables/processing/daily_table --targetSize=10 --groupBy=’.*/hourly_table/.*/(\d\d)/.*\.log’

S3DistCp copies data using distributed map–reduce jobs, which is similar to Hadoop DistCp. S3DistCp runs mappers to compile a list of files to copy to the destination. Once mappers finish compiling a list of files, the reducers perform the actual data copy. 

Generally speaking, the number of mappers is usually 1 and the number of reducers is equal to Maximum allocated yarn memory/Memory allocated to each reducer.

For example, if you have an AWS EMR cluster with 5 "i3.8xlarge" core nodes. An "i3.8xlarge" node has a default of "yarn.scheduler.maximum-allocation-mb" as 241664 and "mapreduce.reduce.memory.mb" as 15104 .These values we can check for each instance type here[1]) meaning that 241664/15104 = 16 reducers that can run in parallel inside a single instance. Since there are 5 core instances on the cluster, 80 reducers can run in parallel. We have to remove from this number 1 reducer (<memory:15104, vCores:1>) to make space for the Application Master (<memory:15104, vCores:1>). So in total, 79 reducers and 1 Application Master can run in parallel.

So as far as improving this performance there a few ways that we can do this. 

First of all, we can increase the parallelism in the reducer side, because the reducer actually copies data to the target. To do this, you can do the following -

----------------
1) Increase the Maximum Allocated Yarn Memory -

  - yarn.scheduler.maximum-allocation-mb

OR 

2) Decrease Memory Allocated to each reducer -

  - mapreduce.reduce.memory.mb
----------------

This can be done by creating a config.json file, and passing it to the EMR cluster when it is created using the mapred-site, for example -

----------------
[
    {
        "Classification": "mapred-site",
        "Properties": {
            "yarn.scheduler.maximum-allocation-mb": "<value>",
            "mapreduce.reduce.memory.mb": "<value>"
        }
    }
]
----------------

Furthermore, a bigger cluster will also accelerate the S3DistCp job because it will have more memory available and it can create more containers(reducer) for copying data in parallel. So it may also be worth considering using more core nodes to run the job.

You can also set the number of reducers in the s3-dist-cp command as below -

----------------
$ s3-dist-cp -Dmapreduce.job.reduces=<no.of reducers> --src=s3://<source bucket>/ --dest=hdfs:///output

However increasing the number of reducers  does not always guarantee the improvement of job performance because data characteristics could be different. We recommend to find the optimized number by running the job against subset of data with different reducer number. This also goes for the configuring the above properties in the mapred-site. It really comes down to fine tuning this, and what fits best with your use case.

Lastly, I would like to leave you with a blog regarding some tips for moving data efficiently using S3DistCp between HDFS and S3[3]. I would specifically like to point you towards the section titled "5. Aggregate files based on a pattern". Hadoop is optimized for reading a fewer number of large files rather than many small files, whether from S3 or HDFS. You can use S3DistCp to aggregate small files into fewer large files of a size that you choose, which can optimize your analysis for both performance and cost.

You can combine small files into bigger files by using a regular expression with the --groupBy option, and the --targetSize which is used to choose the size, in mebibytes (MiB), of the files to create based on the --groupBy option[4]. for example -

----------------
$ s3-dist-cp --src /data/incoming/hourly_table --dest s3://my-tables/processing/daily_table_2017 --targetSize=10 --groupBy=’.*/hourly_table/.*(2017-).*/(\d\d)/.*\.(log)’
----------------

[1] https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-hadoop-task-config.html
[2] https://docs.aws.amazon.com/emr/latest/ReleaseGuide/UsingEMR_s3distcp.html#UsingEMR_s3distcp.options
