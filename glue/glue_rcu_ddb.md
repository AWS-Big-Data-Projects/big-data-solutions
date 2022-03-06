With the below Spark Scala Code provided :


    val datasource0 = glueContext.getCatalogSource(database = "mwx_split_events_prod", tableName = "crawler_mwx_id_lookup_prod_restored", redshiftTmpDir = "", transformationContext = "datasource0").getDynamicFrame()    
    val datasource0 = glueContext.getSource("dynamodb", JsonOptions (s"""{"dynamodb.input.tableName": "mwx_id_lookup_prod_restored", "dynamodb.throughput.read.percent": "0.5", "dynamodb.splits": "20" }""")).getDynamicFrame()


In the above code "dynamodb.throughput.read.percent" is set to "0.5" - this means meaning that spark application ran using Glue ETL will attempt to consume half of the read capacity of the table i.e. mwx_id_lookup_prod . 

Let's assume the DynamoDB table i.e. mwx_id_lookup_prod_restored RCU is set to 2500 currently . Therefore per the spark scala code above when the glue etl will run it will consume max 1250 RCU's . Hence this is the expected behavior with dynamodb.throughput.read.percent" when it is set to "0.5" .
