
Known Error Message : 

    Number of TABLE_VERSION resources exceeds the account limit 1000000 (Service: AWSGlue; Status Code: 400; Error Code: ResourceNumberLimitExceededException; Request ID: 38e9debb-42c5-43a6-b111-a53fa496b2f8)



   The reason one gets the above errorr is due to the limit on the number of table versions per Glue account per region which is 1,000,000 [1]. When we update a table in the Glue Data Catalog, the change history is retained as a version. If there are tables that are updated frequently, the number of versions will increase and the above error may occur.

   In order to overcome the issue, one can use any of the following option.

  Option 1 : [Long term fix] Increase the maximum number of table versions in your account by requesting a quota increase[2] . You can update double the limit as mentioned below form the service Quota[2].

    Recent quota increase → Change quota value: 2000000 → Request 

  Option 2 : [ Short term fix ]  You can delete the old unnecessary versions of tables with Glue BatchDeleteTableVersion API[3][4]. If unnecessary versions are accumulated in more than one table, consider taking a permanent measure and periodically taking inventory of the version history. 

          → Step 1: You can retrieve the all the versions of the a table using the following CLI command:

               aws glue get-table-versions --database-name Your_DataBase_Name --table-name Your_Table_Name

         → Step 2: You can run 'batch-delete-table-version' to delete multiple versions of a table as below: 

              aws glue batch-delete-table-version --database-name Your_DataBase_Name --table-name Your_Table_Name --version-ids 0 1 2


  Option 3: [ To prevent these error proactively ] Additionally, we can prevent the creation of versions during UpdateTable API call, by setting parameter 'skipArchive' to true[5]. By default, UpdateTable always creates an archived version of the table before updating it. However, if skipArchive is set to true, UpdateTable will not create the archived version.



References:
[1] Service Quotas :- https://docs.aws.amazon.com/general/latest/gr/glue.html#limits_glue - Number of table versions per account : 1,000,000
[2] https://console.aws.amazon.com/servicequotas/home/services/glue/quotas/L-337244C9
[3] BatchDeleteTableVersion action (Python: batch_delete_table_version) :- https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-catalog-tables.html#aws-glue-api-catalog-tables-BatchDeleteTableVersion
[4] AWS CLI Command Reference | batch-delete-table-version :- https://docs.aws.amazon.com/cli/latest/reference/glue/batch-delete-table-version.html
[5] AWS Glue SkipArchive https://docs.aws.amazon.com/glue/latest/webapi/API_UpdateTable.html#Glue-UpdateTable-request-SkipArchive
