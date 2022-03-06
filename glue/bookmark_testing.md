    1. First, get the job bookmark status to record the "before": 
		        aws glue get-job-bookmark --job-name "YourJobName"

		2. Then, get the timestamp information of your source files: 
		        aws s3 ls s3://yourdata/sourcepath/

		3. Also get the timestamp information of your destination files (where you will be writing your data to: 
		        aws s3 ls s3://yourdata/output/

		4. Before starting the job run tests, reset the bookmark completely
		        aws glue reset-job-bookmark --job-name "YourJobName"

		5. Confirm its taken effect by looking at the bookmark properties and seeing the reset values: 
		        aws glue get-job-bookmark --job-name "YourJobName"

		6. Now start your job from the CLI: 
		        aws glue start-job-run --job-name "YourJobName"

		7. Once the run completes, check to see if it created new files (it should have):
		        aws s3 ls s3://yourdata/output/

		8. Also check that the bookmarks got updated:
		        aws glue get-job-bookmark --job-name "YourJobName"

		9. Now run the job once more and let us see if the bookmark work: 
		        aws glue start-job-run --job-name "YourJobName"

		10. And check status of the files. There should NOT be any new files.
		        aws s3 ls s3://yourdata/output/ 

		11. But when you check the bookmark, it should have updated:
		        aws get-job-bookmark --job-name "YourJobName"

		12. In your source-folder, add a new additional S3 data file. Now run the job once more: 
		        aws glue start-job-run --job-name "YourJobName"

		13. And let us see if it only processes the new data by checking the S3 output files (there should be new ones): 
		        aws s3 ls s3://yourdata/output/ 

		14. And finally, confirm the bookmark was updated: 
		        aws get-job-bookmark --job-name "YourJobName"
