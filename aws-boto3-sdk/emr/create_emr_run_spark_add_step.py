#Define a S3 bucket to store our files temporarily and check if it exists

def temp_bucket_exists(self, s3):
    try:
        s3.meta.client.head_bucket(Bucket=self.s3_bucket_temp_files)
    except botocore.exceptions.ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            terminate("Bucket for temporary files does not exist")
        terminate("Error while connecting to Bucket")
    return true

#Compress the Python files of the Spark application to a .tar file.

def tar_python_script(self):
    # Create tar.gz file
    t_file = tarfile.open("files/script.tar.gz", 'w:gz')
    # Add Spark script path to tar.gz file
    files = os.listdir(self.path_script)
    for f in files:
        t_file.add(self.path_script + f, arcname=f)
    t_file.close()

#Upload the tar file to the S3 bucket for temporary files

def upload_temp_files(self, s3):
    # Shell file: setup (download S3 files to local machine)
    s3.Object(self.s3_bucket_temp_files, self.job_name + '/setup.sh').put(
       Body=open('files/setup.sh', 'rb'), ContentType='text/x-sh'
    )
    # Shell file: Terminate idle cluster
    s3.Object(self.s3_bucket_temp_files, self.job_name + '/terminate_idle_cluster.sh').put(
        Body=open('files/terminate_idle_cluster.sh', 'rb'), ContentType='text/x-sh'
    )
    # Compressed Python script files (tar.gz)
    s3.Object(self.s3_bucket_temp_files, self.job_name + '/script.tar.gz').put(
        Body=open('files/script.tar.gz', 'rb'), ContentType='application/x-tar'
    )        


def start_spark_cluster(self, c):
    response = c.run_job_flow(
        Name=self.job_name,
        ReleaseLabel="emr-4.4.0",
        Instances={
            'InstanceGroups': [
                {'Name': 'EmrMaster',
                 'Market': 'SPOT',
                 'InstanceRole': 'MASTER',
                 'BidPrice': '0.05',
                 'InstanceType': 'm3.xlarge',
                 'InstanceCount': 1},
                {'Name': 'EmrCore',
                 'Market': 'SPOT',
                 'InstanceRole': 'CORE',
                 'BidPrice': '0.05',
                 'InstanceType': 'm3.xlarge',
                 'InstanceCount': 2}
            ],
            'Ec2KeyName': self.ec2_key_name,
            'KeepJobFlowAliveWhenNoSteps': False
        },
        Applications=[{'Name': 'Hadoop'}, {'Name': 'Spark'}],
        JobFlowRole='EMR_EC2_DefaultRole',
        ServiceRole='EMR_DefaultRole',
        VisibleToAllUsers=True,
        BootstrapActions=[
            {'Name': 'setup',
             'ScriptBootstrapAction': {
                 'Path': 's3n://{}/{}/setup.sh'.format(self.s3_bucket_temp_files, self.job_name),
                 'Args': ['s3://{}/{}'.format(self.s3_bucket_temp_files, self.job_name)]}},
            {'Name': 'idle timeout',
             'ScriptBootstrapAction': {
                 'Path': 's3n://{}/{}/terminate_idle_cluster.sh'.format(self.s3_bucket_temp_files, self.job_name),
                 'Args': ['3600', '300']
                    }
                },
            ],
        )   

#Add a step to the EMR cluster

def step_spark_submit(self, c, arguments):
    response = c.add_job_flow_steps(
        JobFlowId=self.job_flow_id,
        Steps=[{
            'Name': 'Spark Application',
            'ActionOnFailure': 'CANCEL_AND_WAIT',
            'HadoopJarStep': {
               'Jar': 'command-runner.jar',
               'Args': ["spark-submit", "/home/hadoop/run.py", arguments]
            }
        }]
    )

#Describe status of cluster until all steps are finished and cluster is terminated.

def describe_status_until_terminated(self, c):
    stop = False
    while stop is False:
        description = c.describe_cluster(ClusterId=self.job_flow_id)
        state = description['Cluster']['Status']['State']
        if state == 'TERMINATED' or state == 'TERMINATED_WITH_ERRORS':
            stop = True
        print(state)
        time.sleep(30)

#Remove the temporary files from the S3 bucket when the cluster is terminated.


def remove_temp_files(self, s3):
    bucket = s3.Bucket(self.s3_bucket_temp_files)
    for key in bucket.objects.all():
        if key.key.startswith(self.job_name) is True:
            key.delete()

