As an Example - Create a crawler, crawling the  location that your table was located at, and provide a prefix of aws_test to the table to differentiate the table from the existing table. 

On running the crawler, check to see the table getting created in Glue under the database xxxxx And the corresponding table(aws_test_xxxxxxxx) should also be visible in LakeFormation with an IAMAllowedPrincipals rule on the table. 

In order to revoke the permissions on a table in LakeFormation do :- 

I] Select the respective table(From the Tables tab) --> Actions --> View  permissions

II] Select the respective IAM Entity --> Revoke --> Revoke 

In order to grant an IAM Entity,  the permissions on a table in LakeFormation do :- 

I] Select the respective table(From the Tables tab) --> Actions --> View  permissions

II] Grant --> Choose IAM Principals to add --> Database(select the respective Database) --> Select the respective table (column optional, i.e. you can also mention the specific columns  by default the permissions that will be selected in the "Table permissions" will be acting on all the columns present on the table)

Following the above steps you can:- 

1. Remove all the permissions from the table and queried in Athena, this results in failed query due to insufficient LF permissions. 

2. Add the IAMAllowedPrincipals on the table and you were able to query the table from Athena. 

IAMAllowedPrincipals allows all the IAM entities that have the respective S3, Athena and Glue permissions to  successfully query the table and effectively removes the necessity of allowing permissions by adding rules in LakeFormation.
