Exit code: 255
Stack trace: org.apache.hadoop.yarn.server.nodemanager.containermanager.runtime.ContainerExecutionException: Launch container failed
	at org.apache.hadoop.yarn.server.nodemanager.containermanager.linux.runtime.DefaultLinuxContainerRuntime.launchContainer(DefaultLinuxContainerRuntime.java:113)
	at org.apache.hadoop.yarn.server.nodemanager.containermanager.linux.runtime.DelegatingLinuxContainerRuntime.launchContainer(DelegatingLinuxContainerRuntime.java:130)
	at org.apache.hadoop.yarn.server.nodemanager.LinuxContainerExecutor.launchContainer(LinuxContainerExecutor.java:395)
	at org.apache.hadoop.yarn.server.nodemanager.containermanager.launcher.ContainerLaunch.call(ContainerLaunch.java:299)
	at org.apache.hadoop.yarn.server.nodemanager.containermanager.launcher.ContainerLaunch.call(ContainerLaunch.java:83)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
