Instructions: 
---------------

## EC2 instance

1. Install dev stuffs
```
sudo wget https://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo -O /etc/yum.repos.d/epel-apache-maven.repo
sudo sed -i s/\$releasever/6/g /etc/yum.repos.d/epel-apache-maven.repo
sudo yum install -y java-1.8.0-devel git apache-maven patch
sudo /usr/sbin/alternatives --config java
# select java 8
```

2. Build Hive with patch for metastore
```
git clone https://github.com/apache/hive.git
cd hive
git checkout branch-2.3
wget https://issues.apache.org/jira/secure/attachment/12958418/HIVE-12679.branch-2.3.patch
patch -p0 <HIVE-12679.branch-2.3.patch
mvn clean install -DskipTests
```
Take note of the version built. current 2.3.8-SNAPSHOT

3. Build again hive for spark libraries (1.2 metastore)
```
# reset git
git clean -df
git checkout -- .
# build
git checkout branch-1.2
wget https://issues.apache.org/jira/secure/attachment/12958417/HIVE-12679.branch-1.2.patch
patch -p0 <HIVE-12679.branch-1.2.patch
mvn clean install -DskipTests -Phadoop-2
```
Take note of the version built. current: 1.2.3-SNAPSHOT

4. Build AWS Glue client libraries
```
cd /home/ec2-user
git clone https://github.com/awslabs/aws-glue-data-catalog-client-for-apache-hive-metastore.git
cd /home/ec2-user/aws-glue-data-catalog-client-for-apache-hive-metastore/
```

5. Modify the following files to fix compilation issues.

pom.xml (root folder)
- Replace the spark-hive.version with 1.2.3-SNAPSHOT
- Replace the hive2.version with 2.3.8-SNAPSHOT

aws-glue-datacatalog-spark-client/pom.xml
- replace all occurrences of `org.spark-project.hive` with `org.apache.hive`

shims/spark-hive-shims/pom.xml
- replace all occurrences of `org.spark-project.hive` with `org.apache.hive`
- Add the following dependency in `dependencies` tag
```
<dependency>
    <groupId>org.apache.hadoop</groupId>
    <artifactId>hadoop-common</artifactId>
    <version>${hadoop.version}</version>
    <scope>provided</scope>
</dependency>
```

6. Compile
From the root folder. Launch
```
mvn clean package -DskipTests
```
The AWSGlueDataCatalogHive2Client module will fail due to a code issue, but this package is not required for Spark, so we don't care.


7. Install Spark (official version)
```
cd /home/ec2-user/
wget http://archive.apache.org/dist/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz
tar xvzf spark-2.4.4-bin-hadoop2.7.tgz
rm spark-2.4.4-bin-hadoop2.7.tgz
```

8. Configure the Glue Data Catalog Client
vim spark-2.4.4-bin-hadoop2.7/conf/hive-site.xml
```
<configuration>
  <property>
    <name>hive.metastore.connect.retries</name>
    <value>15</value>
  </property>
  <property>
    <name>hive.metastore.client.factory.class</name>
    <value>com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory</value>
  </property>
</configuration>
```

9. Replace the patched Hive libraries in the spark path
```
# replace hive libraries in spark
rm spark-2.4.4-bin-hadoop2.7/jars/hive-exec-*
rm spark-2.4.4-bin-hadoop2.7/jars/hive-metastore-*
cp .m2/repository/org/apache/hive/hive-exec/1.2.3-SNAPSHOT/hive-exec-1.2.3-SNAPSHOT.jar spark-2.4.4-bin-hadoop2.7/jars/
cp .m2/repository/org/apache/hive/hive-metastore/1.2.3-SNAPSHOT/hive-metastore-1.2.3-SNAPSHOT.jar spark-2.4.4-bin-hadoop2.7/jars/
```

10. Add the AWS glue libraries in the spark path
```
cp .m2/repository/com/amazonaws/aws-java-sdk-core/1.11.267/aws-java-sdk-core-1.11.267.jar spark-2.4.4-bin-hadoop2.7/jars/
cp .m2/repository/com/amazonaws/aws-java-sdk-glue/1.11.267/aws-java-sdk-glue-1.11.267.jar spark-2.4.4-bin-hadoop2.7/jars/
cp /home/ec2-user/aws-glue-data-catalog-client-for-apache-hive-metastore/aws-glue-datacatalog-spark-client/target/aws-glue-datacatalog-spark-client-1.10.0-SNAPSHOT.jar spark-2.4.4-bin-hadoop2.7/jars/
```


Note: Configure the the credentials in the .aws/credentials. or if you are running on a EC2 attach a role with Glue Data Catalog Access. 
```
export JAVA_HOME=/usr/lib/jvm/java-1.8.0
export PATH=$PATH:$JAVA_HOME/bin:$JAVA_HOME/jre/bin
export SPARK_HOME=~/spark-2.4.4-bin-hadoop2.7

./spark-2.4.4-bin-hadoop2.7/bin/spark-shell
spark.sql("show databases").show()
spark.sql("show tables in default").show()
```


=========================================================================================================================
