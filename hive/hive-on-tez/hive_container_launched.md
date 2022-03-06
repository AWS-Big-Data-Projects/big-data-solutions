Check Hive server logs 

======Hive server logs=====
2020-06-16T21:20:14,294 INFO  [8c563000-9fde-4280-b549-598dabbaa2ad HiveServer2-HttpHandler-Pool: Thread-35082([])]: session.SessionState (SessionState.java:resetThreadName(436)) - Resetting thread name to  HiveServer2-HttpHandler-Pool: Thread-35082
2020-06-16T21:20:14,351 INFO  [HiveServer2-HttpHandler-Pool: Thread-35082([])]: thrift.ThriftHttpServlet (ThriftHttpServlet.java:doPost(145)) - Could not validate cookie sent, will try to generate a new cookie
2020-06-16T21:20:14,351 INFO  [HiveServer2-HttpHandler-Pool: Thread-35082([])]: thrift.ThriftHttpServlet (ThriftHttpServlet.java:doKerberosAuth(398)) - Failed to authenticate with http/_HOST kerberos principal, trying with hive/_HOST kerberos principal
2020-06-16T21:20:14,351 ERROR [HiveServer2-HttpHandler-Pool: Thread-35082([])]: thrift.ThriftHttpServlet (ThriftHttpServlet.java:doKerberosAuth(406)) - Failed to authenticate with hive/_HOST kerberos principal

Ask yourself these questions : -

if you are using Knox+AD to connect Hive Server2, so there are multiple scenarios for such issues as like-

1. If you are using same AD domain controllers for multiple service then it might have more loads on it.

2. Network lag between KDC and EMR

3. Another thing it might be having issue while using the default fetch-size .

Try the following : -

1. Run the query using mr engine (set hive.execution.engine=mr;) 

2. Run the same query from hive cli 

3. Change the beeline to debug mode then run the query (Please provide the output of console and application ID)

        sudo cp /etc/hive/conf/beeline-log4j2.properties /home/hadoop
        vi beeline-log4j2.properties
        ====change below property===
        status = DEBUG         (default info)
        name = BeelineLog4j2
        packages = org.apache.hadoop.hive.ql.log

        # list of properties
        property.hive.log.level = DEBUG       (default warn)
        property.hive.root.logger = console
        =====

        Run beeline
        beeline -u "jdbc:hive2://......" --poperty-file "/home/hadoop/beeline-log4j2.properties"

4. Try running the same query by increasing the fetch size  (set hive.server2.thrift.resultset.max.fetch.size=2000 (default is 1000)

5. Try running the same query  directly using !connect jdbc:hive2://hostip:port/;principal=hive/HOST_@domainname;transportMode=http;httpPath=cliservice

Note-port for http connection in direct mode will be 1001 (you can verify same from /etc/hive/conf/hive-site.xml hive.server2.thrift.http.port)

