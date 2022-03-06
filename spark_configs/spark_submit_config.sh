-executor-memory = 4g
    --driver-memory=4g
    --spark.driver.memoryOverhead=512
    --spark.executor.memoryOverhead=512


Config Set II:   fails in 5th iteration
      --driver-memory=5g
      --spark.driver.memoryOverhead=1000


Config Set III:
    --executor-memory = 5g
    --driver-memory=5g
    --spark.driver.memoryOverhead=1000
    --spark.executor.memoryOverhead=1000
    --spark.sql.files.maxPartitionBytes=163421772
    --spark.sql.hive.caseSensitiveInferenceMode=NEVER_INFER
    --spark.speculation=false
    --spark.hadoop.fs.s3.maxRetries=3
    --spark.hadoop.fs.s3.consistent.retryPolicyType=exponential
