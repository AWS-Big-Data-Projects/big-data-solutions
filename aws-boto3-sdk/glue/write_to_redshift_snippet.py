datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "mydatabase", table_name = "rs_sample", transformation_ctx = "datasource0")

datasink4 = glueContext.write_dynamic_frame.from_jdbc_conf(frame = dropnullfields3, catalog_connection = "glue_conn", connection_options = {"preactions":"CREATE SCHEMA IF NOT EXISTS test_schema;", "dbtable": "test_schema.rs_sample", "database": "dev", "aws_iam_role": "arn:aws:iam::123456789111:role/redshift_role_servicebased", "mode": "overwrite"}, redshift_tmp_dir = "s3://s3-bucket/redshift_output/", transformation_ctx = "datasink4")
job.commit()
