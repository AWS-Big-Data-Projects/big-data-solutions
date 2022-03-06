import boto3
client = boto3.client(service_name='glue', region_name='us-east-1',
          endpoint_url='https://glue.us-east-1.amazonaws.com') 
response = client.start_job_run(JobName='WHICH U CREATED IN CONSOLE')
status = client.get_job_run(JobName=job_name, RunId=response['JobRunId'])

if status:
    state = status['JobRun']['JobRunState']
    while state not in ['SUCCEEDED']:
        time.sleep(30)
        status = client.get_job_run(JobName=job_name, RunId=response['JobRunId'])
        state = status['JobRun']['JobRunState']
        if state in ['STOPPED', 'FAILED', 'TIMEOUT']:
            raise Exception('Failed to execute glue job: ' + status['JobRun']['ErrorMessage'] + '. State is : ' + state)
