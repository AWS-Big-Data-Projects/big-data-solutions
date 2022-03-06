In case one runs into Throttling with the DDB , it might be a Hot Partition Issue with the DDB . Perform the following steps to check what had caused the same : 

As a first step check the read throttling metrics from the DDB Table UI console : 

ReadThrottleEvents:
    https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#metricsV2:graph=~%28region~%27us-east-1~metrics

Check the DynamoDB logs to see if you have running into throttled requests around the timeframe you had issues with the DDB table. 

Hot Partition Explanation: 

    Each partition on a DynamoDB table is subject to a hard limit of 1,000 write capacity units and 3,000 read capacity units.  If your workload is unevenly distributed across partitions, or if the workload relies on short periods of time with high usage (a burst of read or write activity), the table might be throttled.

    DynamoDB adaptive capacity automatically boosts throughput capacity to high-traffic partitions. However, each partition is still subject to the hard limit. This means that adaptive capacity can't solve larger issues with your table or partition design. To avoid hot partitions and throttling, optimize your table and partition structure. [1][2][3]

    To fix the hot partitions and throttling issue you are experiencing we have few solutions, which I have mentioned below:

    Before implementing one of the following solutions, use Amazon CloudWatch Contributor Insights to find the most accessed and throttled items in your table. Then, use the solutions that best fit your use case to resolve throttling. [4]

                •	Distribute read and write operations as evenly as possible across your table. A hot partition can degrade the overall performance of your table. For more information, see Designing Partition Keys to Distribute Your Workload Evenly. [3]

                •	Implement a caching solution. If your workload is mostly read access to static data, then query results can be delivered much faster if the data is in a well designed cache rather than in a database. DynamoDB Accelerator (DAX) is a caching service that offers fast in memory performance for your application. You can also use Amazon ElastiCache. [5][6]

                •	Implement error retries and exponential backoff. Exponential backoff can improve an application's reliability by using progressively longer waits between retries. If you're using an AWS SDK, this logic is built in. If you're not using an AWS SDK, consider manually implementing exponential backoff. For more information, see Error Retries and Exponential Backoff in AWS. [8]


References:

[1] https://aws.amazon.com/premiumsupport/knowledge-center/dynamodb-table-throttled/
[2] https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html#bp-partition-key-partitions-adaptive
[3] https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html
[4] https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/contributorinsights_HowItWorks.html
[5] https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html
[6] https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/elasticache-use-cases.html
[7] https://docs.aws.amazon.com/general/latest/gr/api-retries.html
