
#creates an EMR with JupyterHub as an application

aws emr create-cluster --name="MyJupyterHubCluster" --release-label emr-5.29.0 \
--applications Name=JupyterHub --log-uri s3://aws-isgaur-logs/AWSLogs \
--use-default-roles --instance-type m5.xlarge --instance-count 2 --ec2-attributes KeyName=training_tst

# Fetches docker Id after doing ssh to Master node of an EMR Cluster

sudo docker ps -


#Login to Docker as sudo

sudo docker exec -it 06550d4c4cc0  /bin/bash


#Restart jupyterhub inside a Docker

sudo docker restart jupyterhub

#Checks Installation for JupyterLab

sudo docker exec jupyterhub bash -c "conda list" | grep -i "jupyterlab"

# To open JupyterLab 

sudo vi /etc/jupyter/conf/jupyterhub_config.py


