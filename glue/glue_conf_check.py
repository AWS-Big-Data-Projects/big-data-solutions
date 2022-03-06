print(sc._conf.getAll())

To set --conf parameters in AWS Glue Spark Job, you can refer the below steps & set the multiple --conf parameters.

    1. Navigate to the 'Script libraries and job parameters (optional)'  from the glue job console -> Job parameters -> enter key/value pair'

    2. Step 2: In Glue Job we can not pass multiple "--conf" values but as a workaround we can use the below method in Job parameter as key/value.
    --
    key: --conf  
    
    value: Spark.executor.memory = 16g --conf Spark.yarn.memoryoverhead = 10g 
    --conf Spark.sql.broadcastTimeout  = 600 
    --conf Spark.sql.autoBroadcastJoinThreshold = 50485760
    --conf Spark.dynamicAllocation.minExecutors 20

Therefore define only one job parameter with "Key" as --conf followed by value in "Value" input box with other --conf parameters in the same "Value" box.
