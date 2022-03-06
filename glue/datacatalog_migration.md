Unfortunately, there is no built-in solution to migrate glue databases and tables across accounts, and it would need a custom solution.Following are some of the options you can explore : 


1-1. Manually migrate the metadata using Glue APIs 

     In this two-part process, you need to use Glue APIs like GetDatabases, GetTables, GetPartitions, GetConnections and GetUserDefinedFunctions to retrieve and store the metadata information onto an intermediate storage like S3.  Then use their corresponding CreateTable APIs (similar APIs for other corresponding Get-calls) at the other account to recreate the Data Catalog.

1-2. GitHub Script for cross-account Glue Catalog replication [2]

    I found a thread [1] which talks about a solution on Github [2] and uses ETL jobs to migrate Glue catalog from one account to another. I also found a third party [3] blog mentioning backup and restore of glue catalog with Python. You can refer to these solutions for your use case of migration.There is an example on GitHub[2] where they discuss a solution for moving the Catalog between two accounts. It uses two ETL jobs to export the entire data catalog from one account and import it in another account using S3 as an intermediate storage. Please note that this script isn't supported by AWS, officially. You'll need to test the script and modify it according to your scenario.

1-3 : Using start_query_execution API[4]. You would have to build custom solution to get the tables first within a given Glue database and then use this specific API to run multiple SQL queries ( show create table <table-name>  ) one by one and then get the DDL as an output. 




References:
[1] https://forums.aws.amazon.com/thread.jspa?messageID=942813
[2] https://github.com/aws-samples/aws-glue-samples/tree/master/utilities/Hive_metastore_migration#aws-glue-data-catalog-to-another-aws-glue-data-catalog
[3] https://www.redaelli.org/matteo/posts/how-to-backup-and-restore-glue-data-catalog/
[4] https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.start_query_execution
