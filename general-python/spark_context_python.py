def init_spark():
    import findspark
    findspark.init("/usr/lib/spark/")
    from pyspark.sql import SparkSession
    spark = (
        SparkSession.builder
            .master("yarn")
            .appName("Stage.py")
            .getOrCreate()
    )
    return spark

spark = init_spark()
