However, looking at the last screenshot provided, I can see that they are all set to the "Sum" statistic. While this can be useful, it can also be quite misleading on its own as to the actual behavior of your DynamoDB table.

 The following statistics are valid and important for discerning an accurate behavior of your DDB table:
 
    - Maximum = This statistic is the largest value detected within the set period.
    - Minimum = This statistic is the smallest value detected within the set period.
    - Average = This statistic is the average value detected within the set period.
    - Sample Count = The number of requests made within the period.

No one statistic is enough to show the full behavior, but instead these 4 statistics are used together to paint an overall picture of the behavior of your table.

"Average" is perhaps the best statistic to use to determine the current running latency, but I would also advise to keep an eye on the others from time-to-time.

So, as an example, say I had the following latency values (in milliseconds) over a 1-minute period (say executing 1 request every second):

    1, 2, 1, 1, 4, 3, 1, 2, 1, 3, 3, 2, 2, 1, 3,
    15, 2, 7, 6, 8, 4000, 1, 2, 1, 3, 3, 2, 2, 1, 3,
    1, 2, 1, 1, 4, 3, 1, 2, 1, 3, 3, 2, 2, 1, 3,
    1, 2, 1, 1, 4, 3, 1, 2, 1, 3, 3, 2, 2, 1, 3,

    If we look at the valid statistic information for this sample set, we would get:

    - Maximum = 4000ms
    - Minimum = 1ms
    - Average = 69.1ms (4146 / 60)
    - Sample Count = 60

So while we got a brief spike to 4000ms here at one second, the rest of the statistics were fine. This would indicate a transient issue for which DDB would re-issue/reprocess the request and return a value to the requester within a lower time that what CloudWatch detected. This would only be an issue if there was a rising pattern of samples or a few continuous samples at this time period.There can be a scenario when maximum latency can go bit high, it is because at the selected time frame even if one of request went high, then this is skewed. 

While the average may seem to still be high (69.1ms), this is because of the size of the sample set used above (60 samples over 1 minute). In a normal workload of a few hundred/thousand requests per minute, the single maximum spike would not have as great an impact on our Average.

In other words, if we had 1000 requests within the minute, and only 1x 4000ms sample, then the average would only increase a much smaller amount:

With 999 samples at 3ms, and 1 sample at 4000ms, the average would be 6.97ms instead of 3ms - a negligible statistical difference for DDB latency.

Everything looks good from the above statistics for the p90 metrics.

DynamoDB has very high availability and durability, but occasionally there are some backend processes that need to happen in order to maintain an extremely high level of reliability. In these occasions, customers can sometimes see what appears to be an occasional/sporadic "spike" in the Maximum statistic.

However, with that said, DynamoDB also has numerous fail-overs and safeguards to protect our customers latencies in these instances. Requests will be retried/reprocessed in a very quick fashion and the results returned to the requester. This is why while the "Maximum" statistic may "spike" occasionally, as long as the "Minimum" and "Average" statistics remain stable then it is not a cause for concern.

We can see this behavior in your CloudWatch metrics as below of your usage with your DDB table.

SuccessfulRequestLatency  - Batch GetITem 

<>

=================
Recommendation 
=================

Consider one or more of the following strategies to reduce latency:

    1. Reduce the request timeout settings: Tune the client SDK parameters requestTimeOut and clientExecutionTimeout to timeout and fail much faster (for example, after 50 ms). This causes the client to abandon high latency requests after the specified time period and then send a second request that usually completes much faster than the first. For more information about timeout settings, see Tuning AWS Java SDK HTTP request settings for latency-aware Amazon DynamoDB applications.[1]

    2. Reduce the distance between the client and the DynamoDB endpoint: If you have globally dispersed users, consider using global tables[2]. With global tables you can specify the AWS Regions where you want the table to be available. This can significantly reduce latency for your users.

    3. Use caching: If your traffic is read heavy, consider using a caching service such as DynamoDB Accelerator (DAX)[3]. DAX is a fully managed, highly available, in-memory cache for DynamoDB that delivers up to a 10x performance improvement—from milliseconds to microseconds—even at millions of requests per second.

    4. Send constant traffic or reuse connections: When you're not making requests, consider having the client send dummy traffic to a DynamoDB table. Alternatively, you can reuse client connections or use connection pooling. All of these techniques keep internal caches warm, which helps keep latency low.

    5. Use eventually consistent reads: If your application doesn't require strongly consistent reads, consider using eventually consistent reads. Eventually consistent reads are cheaper and are less likely to experience high latency. For more information, see Read Consistency.[4]

===============
Conclusion 
==============


    From the p99 metrics, we can see the latency on DynamoDB was below 10ms. This means the average of 99% of the request was below 10ms.

    What would be of concern is if your "Average" statistic rose sharply in a pattern over a period for multiple time frame. In this spike reported for the batch get latency on 11/11/2020 around 16:14 UTC, it is not the case.

    When analyzing the Amazon CloudWatch metric SuccessfulRequestLatency, it's a best practice to check the average latency. Occasional spikes in latency are not a cause for concern. However, if average latency is high over a period of time continuously, there might be an underlying issue that you need to resolve.This table seem to be healthy and operational performance seems to be in the expected zone. There are a lot of factors that go into the latency when making a call to DynamoDB. DynamoDB can provide latency in the single digit milliseconds but there are some caveats where it can not perform at that level on a small factor. If p99 latency is below 10ms, it means it is performing well.
