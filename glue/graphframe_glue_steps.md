

Run these on a EC2 

1. we need to get the Graphframes code from either Github / PyPi : (https://pypi.org/project/graphframes/#files)
2. Download the tar file on a EC2 instance. 
3.  Untar  (tar -xvf)
4. cd into the folder. and zip the contents into a zip file. I called it as graphframes.zip. Make sure that the graphframes are a direcly a part of the zip file and not under a folder when zipping. 
5. Upload graphframes.zip to S3

6. Upload the downloaded graphframes zip file to an S3 location.

7. Create a new Glue job via AWS console.

8. Under 'Python Library Path' section of  'Script libraries and job parameters (optional)' section, add the S3 location of the graphframes package file(zip file).

9. Under 'Job Parameters' section of 'Script libraries and job parameters(optional)' section, enter the following:
Key: --conf
Value: spark.jars.packages=graphframes:graphframes:0.6.0-spark2.3-s_2.11

10. Run a sample code to import 'graphframe' package and use GraphFrame class. I have attached a sample script(graph_sample) for your reference.
Please refer to the screenshots that I have attached to help you with step 3 and step4.

Please note that some of the algorithms in graphframe package requires setting a Spark checkpoint directory, which can be performed by using the following line in your code.

" SparkContext.setCheckpointDir('<path>') "

Also, note that <path> must be a hdfs path. For example, you can use 'user/hadoop/' or '/tmp/'.
