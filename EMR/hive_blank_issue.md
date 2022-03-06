<property>
  <name>hive.metastore.orm.retrieveMapNullsAsEmptyStrings</name>
  <value>true</value>
</property>


Test Data => 

251|Paris Hotel|Las Vegas|NV|
258|Tropicana Hotel|Las Vegas|NV|
300|Kennedy Center Opera House|Washington|DC|0
306|Lyric Opera House|Baltimore|MD|0
308|Metropolitan Opera|New York City|NY|0
22|Quicken Loans Arena|Cleveland||0
101|Progressive Field|Cleveland||43345

Create table in Hive => 

      CREATE EXTERNAL TABLE `ajinkya.ajinkya_tests_new2`(
       `id` bigint, 
       `name` string, 
       `state` string, 
       `city` string, 
       `zip` bigint)
      ROW FORMAT SERDE 
       'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe' 
      WITH SERDEPROPERTIES ( 
       'field.delim'='|', 
       'line.delim'='\n', 
       'serialization.format'='|', 
       'serialization.null.format'='') 
      STORED AS INPUTFORMAT 
       'org.apache.hadoop.mapred.TextInputFormat' 
      OUTPUTFORMAT 
       'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
      LOCATION
       's3://xx-xx/ajinkya_tests';

> select * from ajinkya.ajinkya_tests_new where city is null;
    OK
    Time taken: 0.442 seconds
    hive> 

Config 1 Change -

 Either set the value in hivesite.xml .Path for hivesite.xml on emr cluster - /etc/hive/conf/hive-ste.xml

or setting the property using beeline at the session level or hive session - > 

     set hive.metastore.orm.retrieveMapNullsAsEmptyStrings=true;

Config 2 => set 'serialization.null.format'='' setting this property while table creation.

Testing =>  > select * from ajinkya.ajinkya_tests_new2 where city is null;
OK
22	Quicken Loans Arena	Cleveland	NULL	0
101	Progressive Field	Cleveland	NULL	43345
Time taken: 0.355 seconds, Fetched: 2 row(s)
hive> 

> select * from ajinkya.ajinkya_tests_new2 where length(trim(city))=0;
OK
Time taken: 0.353 seconds
hive>

> select * from ajinkya.ajinkya_tests_new2 where city ='';
OK
