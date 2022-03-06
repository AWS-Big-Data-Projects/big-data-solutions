CREATE EXTERNAL TABLE hivejson_wdcc (
  sysdate string,
  referrer string,
  clientip string,
  queryString map<string,string>
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
LOCATION
  's3://pl200620-ap121142-pzn-kinesisfirehose-dev/kafkahive/';

select querystring['p0'],querystring['vsdr'] from hivejson_wdcc;
--> 41
