To load the timestamp with timezone 

datasink4 = glueContext.write_dynamic_frame.from_jdbc_conf(frame = persons_DyF, catalog_connection = "test", connection_options = {"dbtable": "testalblog2", "database": "reddb","postactions":"delete from emp1;","extracopyoptions":"TIMEFORMAT 'auto'"},
redshift_tmp_dir = 's3://s3path', transformation_ctx = "datasink4")
