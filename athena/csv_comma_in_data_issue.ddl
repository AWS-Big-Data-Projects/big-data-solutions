======================================

CREATE EXTERNAL TABLE `test`(
  `title` string COMMENT 'from deserializer', 
  `field_pso_number` string COMMENT 'from deserializer', 
  `field_address` string COMMENT 'from deserializer', 
  `field_phone` string COMMENT 'from deserializer', 
  `field_phone_ext` string COMMENT 'from deserializer', 
  `field_state` string COMMENT 'from deserializer', 
  `view_node` string COMMENT 'from deserializer')
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.OpenCSVSerde' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://your-s3-bucket/path/to/csvfile';

======================================= 
