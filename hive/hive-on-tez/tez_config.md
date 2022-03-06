As far as my experience goes  , I would focus on these properties to optimize the TEZ workloads . I always recommend setting these TEZ properties at the Hive session level first and monitor the hive query execution progress for a certain number of days ( 3-4 days ) :

1. This parameter control the number of mappers for splittable formats with Tez - 

          set tez.grouping.min-size = 167772;

2. Container Size => 

          set hive.tez.container.size=10752;
      
3. Heap size => 

          set hive.tez.java.opts=-Xmx8600m;
    
4. TEZ Application master and Container Java Heap sizes => 

          set tez.am.resource.memory.mb=15360;
          set tez.am.launch.cmd-opts=-Xmx12288m; 

References : 

[1] https://community.cloudera.com/t5/Community-Articles/Demystify-Apache-Tez-Memory-Tuning-Step-by-Step/ta-p/245279
[2] https://community.cloudera.com/t5/Community-Articles/Hive-on-Tez-Performance-Tuning-Determining-Reducer-Counts/ta-p/245680
