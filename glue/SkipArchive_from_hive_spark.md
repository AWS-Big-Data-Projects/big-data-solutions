As of today there is no way to set parameter 'skipArchive' while using Hive/Spark from AWS EMR pointing to AWS glue Data catalog.


Workarounds:

1) Drop the table and recreate it.

    For example:
    =============
        aws glue get-table --database-name <value> --name <value> --region <region_name> > /tmp/table.json
        aws glue create-table --database-name <value> --region <value> --table-input file:///tmp/table-tmp.json
    ============

2) Delete the versions using the delete-table-version API

      You can retrieve the all the versions of the a table using the following CLI command:
      ============
      aws glue get-table-versions --database-name Your_DataBase_Name --table-name Your_Table_Name
      ============

      And then you can run 'batch-delete-table-version' to delete multiple versions of a table as below: 
      ============  
      aws glue batch-delete-table-version --database-name Your_DataBase_Name --table-name Your_Table_Name --version-ids 0 1 2
      ============

3) Increase TABLE_VERSION resources service limit 

      TABLE_VERSION resources service limit is a soft limit and can be lifted.
