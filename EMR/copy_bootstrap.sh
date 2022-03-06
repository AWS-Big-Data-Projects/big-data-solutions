#!/bin/bash
set -x
aws s3 cp s3://aws-xxx-logs/python_jupyter/satish_install_new.sh /home/hadoop/satish_install_new.sh && sudo bash /home/hadoop/satish_install_new.sh & exit 0
