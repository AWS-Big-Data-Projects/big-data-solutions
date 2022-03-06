## How to pass proxy parameters for spark applications which write through EMRFS.

This can be done as below for SPARK command.

spark-shell --conf spark.driver.extraJavaOptions=-Dhttp.proxyHost=myproxy.host.com -Dhttp.proxyPort=80 -Dhttps.proxyHost=myproxy.host.com -Dhttps.proxyPort=80” —conf spark.hadoop.fs.s3a.access.key=$AWS_ACCESS_KEY_ID --conf spark.hadoop.fs.s3a.secret.key=$AWS_SECRET_ACCESS_KEY
