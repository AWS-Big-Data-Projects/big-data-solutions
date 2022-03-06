Apply Configuration while Launching an EMR - 

        [
            {
                "Classification": "spark-hive-site",
                "Properties": {
                    "hive.metastore.client.factory.class": "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory",
                    "aws.region": "us-east-1"
                }
            },
            {
                "Classification": "hive-site",
                "Properties": {
                    "hive.metastore.client.factory.class": "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory",
                    "aws.region": "us-east-1"
                }
            },
            {
                "classification": "hdfs-site",
                "properties": {
                    "aws.glue.endpoint": "glue.us-east-1.amazonaws.com"
                },
                "configurations": []
            }
        ]


Apply Configuration on Running EMR Cluster - 

        Modify the "/etc/hadoop/conf/hdfs-site.xml" and add the following property

          <property>
            <name>aws.glue.endpoint</name>
            <value>glue.<REGION_OF_GLUE_TABLE>.amazonaws.com</value>
          </property>

         Restart hive and hcatalog services - 

          $ sudo service hive-server2 stop 
          $ sudo service hive-hcatalog-server stop
          $ sudo service hive-server2 start
          $ sudo service hive-hcatalog-server start
