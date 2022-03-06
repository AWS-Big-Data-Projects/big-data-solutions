connection_options using from_catalog :

-------------
connection_options = {
    "query": "SELECT * FROM public.users WHERE userid=3", #This should be the schema name and table name in the Redshift source
    "aws_iam_role": "arn:aws:iam::my_account_id:role/MyRedshiftRole"
}
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "my_glue_database", table_name = "my_glue_table", redshift_tmp_dir = args["TempDir"], additional_options = connection_options, transformation_ctx = "datasource0")
-------------


connection_options using create_dynamic_frame_from_options :
 
-------------
connection_options = {
    "url": "jdbc:redshift://redshift-cluster-1.xxxxx.us-east-1.redshift.amazonaws.com:5439/dev",
    "query": "SELECT * FROM public.users WHERE userid=3",
    "user": "myuser",
    "password": "password",
    "redshiftTmpDir": "s3://mybucket/tmp/",
    "aws_iam_role": "arn:aws:iam::my_account_id:role/MyRedshiftRole"
}
    
dynf_records = glueContext.create_dynamic_frame_from_options("redshift", connection_options)
dynf_records.count()
