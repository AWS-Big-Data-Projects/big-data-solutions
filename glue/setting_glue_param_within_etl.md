---------------------------
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
sparkSession = spark.builder.config('spark.sql.sources.partitionColumnTypeInference.enabled', False).config('spark.driver.memory', '7g').config('spark.executor.memory', '5g').config('spark.speculation',False).getOrCreate()
---------------------------


print("Spark Parametsr passed:", spark.sparkContext.getConf().getAll()),  in my glue job, I was able to verify that the parameters were populated correctly.
