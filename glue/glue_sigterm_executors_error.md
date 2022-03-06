====
20/01/17 19:04:22 ERROR CoarseGrainedExecutorBackend: RECEIVED SIGNAL TERM 
====

SIGTERM is usually received due to memory overutilization, using the bigger Worker types,  will let you have much larger memory allocation for them.

If you see , the job is running with a single executor for most of its lifetime, peaking at only as an example 5 or 6 executors at some point. 

For reference, with the 50 DPUs and the Standard worker type you configure for your job, you should be getting a maximum of 97 executors - which means your resources are being wasted. This also explains why your executors are running out of memory - instead of distributing the dataset amongst them, only a few are trying to load it entirely and failing to do so.

This proves the reads are not parallelized. I would recommend following our documentation to achieve this: [1]. If you follow the guidelines on our capacity planning section [2], you'll see you should be setting a minimum of 388 Spark partitions (parallel reads) for your job to fully utilize the 50 DPUs. This should divide the dataset across all of your executors, which will decrease memory pressure on them, and in the end make your job run properly.

For now I would suggest simply making sure there's parallel reads, which should get you a nice number of executors at the start. Then the default number of partitions after a join should keep that number, so you can try to apply the changes stated in the documentation link mentioned before and run again to see how it goes. If the job fails again, check the executor count metric. If it goes low again you'll have to check your code to see if there's any step at which the partition count can be going low (most likely a join) and you can repartition after it. 

[1] https://docs.aws.amazon.com/glue/latest/dg/run-jdbc-parallel-read-job.html
[2] https://docs.aws.amazon.com/glue/latest/dg/monitor-debug-capacity.html
