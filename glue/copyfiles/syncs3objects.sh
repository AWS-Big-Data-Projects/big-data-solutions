#!/bin/bash

aws configure set default.s3.max_concurrent_requests 1000
aws configure set default.s3.max_queue_size 10000

bucket=$1
key=$2
target_path=$3

# echo "aws s3 sync s3://$bucket/$key/ s3://$target_path/"
aws s3 sync s3://$bucket/$key/ s3://$target_path/
