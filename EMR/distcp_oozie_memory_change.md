Here are the different approach(s) to change the mapper and reducer memory of s3-dist-cp job that involves hive job executions.

Option 1- setting the following properties on the script level. An example of hive hql is given below with property values added on it.

======example script=======
--disable blob optimization
set hive.blobstore.optimizations.enabled=false;

--setting tez container size
set hive.tez.container.size=4096;

--setting s3-dist-cp map and reduce memory (default value is 1024MB)
set mapred.job.map.memory.mb=1400;              
set mapred.job.reduce.memory.mb=1400;

--hive script
drop table ddd;
create table ddd like d;
alter table ddd set location 's3://bucketname/ddd';
insert overwrite table ddd select * from d;

===========

Option 2. Updating hadoop-distcp-2.8.5-amzn-4.jar and uploading into the Oozie workflow lib path
 
 1. SSH to master node
 2.  sudo cp /usr/lib/hadoop/hadoop-distcp-2.8.5-amzn-4.jar /home/hadoop
 3.  jar xf hadoop-distcp-2.8.5-amzn-5.jar distcp-default.xml .
 4.  Edit vi distcp-default.xml and update the value for below propriety as follows-
        <property>
              <name>mapred.job.map.memory.mb</name>
              <value>1400</value>
          </property>

          <property>
              <name>mapred.job.reduce.memory.mb</name>
              <value>1400</value>
          </property>

 5. Run $jar -uf hadoop-distcp-2.8.5-amzn-4.jar distcp-default.xml

 6. Move jar to hdfs or oozie lib location in hdfs as like $hdfs dfs -put hadoop-distcp-2.8.5-amzn-4.jar  /user/${user.name}/share/lib

===job properties
oozie.libpath=/user/${user.name}/share/lib
oozie.use.system.libpath=true


This can be validated from container logs and you can search from "memory" on the log or below sentence-

====
org.apache.hadoop.mapreduce.v2.app.rm.RMContainerAllocator: mapResourceRequest:<memory:1400, vCores:1>

Note- 
Above are the random values for these property, so suggest you to change the appropriate values.
