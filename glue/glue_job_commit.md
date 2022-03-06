The method job.commit() can be called multiple times and it would not throw any error 
as well. However, if job.commit() would be called multiple times in a Glue script 
then job bookmark will be updated only once in a single job run that would be after 
the first time when job.commit() gets called and the other calls for job.commit() 
would be ignored by the bookmark. Hence, job bookmark may get stuck in a loop and 
would not able to work well with multiple job.commit(). Thus, I would recommend you 
to use job.commit() once in the Glue script.
