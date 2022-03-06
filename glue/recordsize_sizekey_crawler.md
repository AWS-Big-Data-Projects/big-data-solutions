** One of my  "raw" named table created by crawler has below property set. It shows "recordCount" as "3554". 

However when I query same table from Athena record count are "25200", so basically "recordCount" metadata used by Crawler to detect schema and real record count in source data is different. 

In general when crawler runs to determine specific table format [1], for some formats reads the beginning of the file to determine format. Example : For JSON format "Reads the beginning of the file to determine format."[1] while determining schema and crawler update these properties.

As it is reading beginning of file, it estimates this metadata for its internal use only. For my example table, I also see averageRecordSize = sizeKey/recordCount, 3071623/3554 = 864.2720 ~ 864. These calculations are internal to Crawler working and it may differ by formats. 



++ Sample table "raw" created by Glue crawler. 
=============================================
Table properties - JSON classification	
sizeKey 3071623
objectCount 2
UPDATED_BY_CRAWLER thermostat-data-crawler
CrawlerSchemaSerializerVersion 1.0
recordCount 3554
averageRecordSize 864
=============================================

++ Sample Athena query :
=============================================
SELECT count(*) FROM "awsblogsgluedemo"."raw"
>> Results
_col0
1	25200
=============================================
