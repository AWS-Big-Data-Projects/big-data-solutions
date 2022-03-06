CREATE TABLE test_multi 
(a string, b string, c string, d string, e string, f string) 
ROW FORMAT SERDE 'org.apache.hadoop.hive.contrib.serde2.MultiDelimitSerDe' 
WITH SERDEPROPERTIES (
    "field.delim"="~|`",
    "collection.delim"=":",
    "mapkey.delim"="@"
);

This is the preferred way of loading multi-character delimited data into Hive over the use of “org.apache.hadoop.hive.serde2.RegexSerDe”, as it is simpler and faster.
