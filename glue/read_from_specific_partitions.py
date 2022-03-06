
In the following example, the job processes data in the s3://awsexamplebucket/product_category=Video partition only:

    datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "testdata", table_name = "sampletable", transformation_ctx = "datasource0",push_down_predicate = "(product_category == 'Video')")

In this example, the job processes data in the s3://awsexamplebucket/year=2019/month=08/day=02 partition only:

    datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "testdata", table_name = "sampletable", transformation_ctx = "datasource0",push_down_predicate = "(year == '2019' and month == '08' and day == '02')")


For non-Hive style partitions. In this example, the job processes data in the s3://awsexamplebucket/2019/07/03 partition only:

    datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "testdata", table_name = "sampletable", transformation_ctx = "datasource0",push_down_predicate ="(partition_0 == '2019' and partition_1 == '07' and partition_2 == '03')" )

