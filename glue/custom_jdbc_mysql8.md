1. Create Glue JDBC connection for JDBC. Fill the correct syntax, but do not worry about the details because they will not be used. The important part is the Security Group, VPC and Subnet to ensure the cluster networking is created correctly to reach the database.

2. Upload the attached Jar into an S3 directory and please make sure your Glue Role have access to that s3 directory.

3. Edit your Glue Job and under the Security Configuration, select the jar under the "Dependent jars path".

4. Now edit your job script. To use the driver to read your table[1], you will need to use the following additional code: 

Code Snippet - Please modify the below.
========================================================
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
connection_mysql8_options = {
    "url": "jdbc:mysql://<jdbc-host-name>:3306/db",
    "dbtable": "test",
    "user": "admin",
    "password": "pwd",
    "customJdbcDriverS3Path": "s3://path/mysql-connector-java-8.0.17.jar",
    "customJdbcDriverClassName": "com.mysql.cj.jdbc.Driver"}

df_mysql8 = glueContext.create_dynamic_frame.from_options(connection_type="mysql",connection_options=connection_mysql8_options)
### rest of the code
========================================================

6. Run this ETL job and please test it. 
