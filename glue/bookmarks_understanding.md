I came across alot of questions on the bookmarks functioning in GlueETL .Here are some of them with answers :

Q.1 When using bookmarks in Glue, I understand the offsets are stored in the glue temp directory specified at job creation. Based on the value you pass into your dynamic_frame via transformation_ctx, it reads the offset and only processes new files created since that job run. I have a few questions on this. Is my understanding correct?

    A - Its partially correct . Unfortunately, as an AWS Premium support Engineer I cannot share the internals(Architecture) of how AWS Glue Job bookmarks stores the State information But I can still share how it works ( functionality) within AWS GlueETL Job.I will try to answer your questions to the best of my knowledge. 

    A Job Bookmark captures the state of job. It is composed of states for various elements of the jobs, i.e. sources, transformations, and sinks.It ensures that if a job is run after a previous successful run it will continue from that point. And if a job is run after a previous failed run it will process the data that it failed to process in the previous attempt .AWS Glue Job bookmarks provide an ability to associate state with a job. This is useful in cases when a job needs to do stateful processing.  Each instance of the state is keyed by a job name and a version number.When a script invokes job.init() it retrieves its state and always gets the latest version. Within a state, there are multiple state elements, which are specific to each source, transformation and sink instances in the script. These state elements are identified by transformation context (*transformation_ctx*) attached to the corresponding element (source, transformation or sink) in the script.  The state elements are saved atomically when job.commit is invoked from the user script. 


Q.2. Does this mean that you can support multiple offsets per job by passing in a different transformation_ctx for each dynamic_frame that needs to be created?

    A - Yes AWS GlueETL can support multiple "transformation_ctx" per job by passing in different transformation_ctx for each dynamic frame.It is supported. I do see Code example provided by you i.e.   


          inputDyf = glueContext.create_dynamic_frame_from_options(connection_type = 's3', connection_options = {'paths': ['s3://' + rawS3BucketName], 'groupFiles': 'none', 'recurse':True}, format = FILE_FORMAT_RAW,format_options=FORMAT_OPTIONS,transformation_ctx = (dbName + "-" + tableName))

    In the above Code example the "transformation_ctx" is parameterized using dbName + "-" + tableName . This is totally supported and will resolve to the relevant "transformation_ctx" per the values passed.

Q.3. Case Scenario: Lets say I trigger JOB A with TRANSFORMATION_CTX A only, and it updates the bookmark. Now lets assume I trigger JOB A for TRANSFORMATION_CTX B only, and it updates the bookmark for this transformation_ctx only. On the third run, if I trigger it for TRANSFORMATION_CTX A again, will the job be smart enough to find the most recent offset for TRANSFORMATION_CTX A? Or is the offset lost since the second run (The one processing ONLY TRANSFORMATION_CTX B) did not process TRANSFORMATION_CTX A?

    A - 1st Run => JOB A with ->  TRANSFORMATION_CTX A only -> Updates the bookmark for TRANSFORMATION_CTX A
        2nd Run => JOB A for TRANSFORMATION_CTX B only => Updates the bookmark for TRANSFORMATION_CTX B
        3rd Run => trigger JOB A for TRANSFORMATION_CTX A again => Yes I can confirm 100% ,it will find the most recent data processed for TRANSFORMATION_CTX A automatically and process the data which is not processed last time. No Offset is lost. As long as the data source for TRANSFORMATION_CTX A vs TRANSFORMATION_CTX B are different ,job bookmarks will work as expected. Hence I assume the data source you would process in 1st and 2nd Run are different. If it's the same Data source for bothTRANSFORMATION_CTX  this will not work as Intended.
        
        
Q.4. How would bookmark rewinding work in this scenario? If I rewind the bookmark to an earlier run for TRANSFORMATION_CTX B, would it also rewind for future TRANSFORMATION_CTX A runs?

    A - When you rewind the job bookmarks - It will revert the state to the previous bookmarked run.to answer your questions if you rewind the bookmark to an earlier run i.e. 2nd Run that I mentioned in my previous response#3 it will only revert the state for TRANSFORMATION_CTX B since you did not process the data for TRANSFORMATION_CTX A in the 2nd run. so to answer you question - No it will not rewind the bookmark state for TRANSFORMATION_CTX A.


Q.5. Finally, IF the offset is lost for TRANSFORMATION_CTX A in question 3, OR if the bookmark will also rewind for TRANSFORMATION_CTX A in question 4, how can I externally track what files have been processed in glue (Ideally based on the INSERT timestamp metadata in S3) using Glue and PySpark? Then, how can read a DataFrame or DynamicFrame based on this offset? Essentially, I would need a way to externally track offset for files processed in Glue from S3. 

    A - No the offset would not be lost for TRANSFORMATION_CTX A in question 3 , neither the bookmark rewind the state for TRANSFORMATION_CTX A in question 4.

    There is no such feature or an option available today to externally track the timestamp/offset for the files processed in glue from S3 . It is not supported. There can be a basic approach you would think of i.e. store the start time of last completed job or process any files with the last modified timestamp > last completed time But this can lead to s3 inconsistency issues with incorrect results. 

Hence I highly recommend to use AWS Glue Job Bookmarks to track the data that had been processed. I hope all the information provided above clarifies your doubts about the AWS glue Job bookmarks.For more details and functionality please refer our AWS docs here.[1]



References:
[1] https://docs.aws.amazon.com/glue/latest/dg/monitor-debug-multiple.html
