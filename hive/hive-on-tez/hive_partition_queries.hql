#creating a hive partitioned table

create table drop_partition (
  id                int,
  name              string
)
partitioned by (city string,country string)
location 's3://aws-isgaur-logs/drop_partition/';

#Inserting a record into a hive table

INSERT INTO TABLE emr7 PARTITION (city='sfo',country='usa') values (123,'ishan');

#Dropping a partition from a hive table

alter table employee drop partition ( city='sfo');


CREATE TABLE glue_tony (
  name string )
PARTITIONED BY (
  year string,
  month string,
  day string)
LOCATION
  's3://aws-isgaur-logs/glue_pd'

  insert into table glue_tony PARTITION (year='2020',month='01',day='01') values (123);

alter table drop_partition drop partition ( city='sydney',country='australia');

INSERT INTO TABLE drop_partition PARTITION (city='sydney',country='australia') values (777,'sam');
