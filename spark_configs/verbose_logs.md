How do I add verbose logs for Spark Driver and Executor?

Since Spark application runs on JVM, the --verbose and the --verbose:class options are both available.


Two switches are relevant in this context. The --verbose option provides configuration details and --verbose:class option reveals the classes loaded by the driver and executor. This debugging utility helps you trace class path conflicts for driver and executor.

1) To list the classes loaded by JVM while running a Java program, use --verbose option. The output is a list of all the classes loaded by the Class loader and the source that called the class. The following is a sample code using the --verbose:class option.

./spark-shell  --conf "spark.executor.extraJavaOptions=-verbose:class"  --conf "spark.driver.extraJavaOptions=-verbose:class"


2) To launch the spark-shell or to run a Spark program using spark-submit, use --verbose option. The --verbose option outputs fine-grained debugging information like where the application loading source.

./spark-shell --verbose
