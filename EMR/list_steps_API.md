
I would like to mention that this error on rate exceeded comes when the API calls being made is more than the current limit. Since EMR is a shared service, we implement certain limits on the APIs "PER account PER region"  to ensure the service is performing correctly and not overloaded. It does not count per cluster or step.

Here you can see the list of the default API rate limits to the EMR service for your reference :[1]. We could see the below limits for ListStepss API call here[1] -

API Action 	    | Bucket Maximum Capacity | Bucket Refill Rate (per second)
ListStepss      |10                       | 0.5

To give you a better understanding about it, I'll explain it briefly. As a starting point, an AWS account can use up to the amount of calls allotted for that specific API call until it runs out. At the same time, this quota is refilled at a specific rate. So if the user makes the same call, on average, at the same rate or less than this refill rate, you should be okay. Throttling can happen if your account is making more calls faster than the refill rate.

In more detail :

for ListSteps = Bucket Size: 10, Refill Rate (per second) 0.5 . What these numbers mean is that you initially have a bucket of 10 ListSteps calls. That number is fixed but as you make ListSteps calls that bucket is refilled at a rate of 0.5 call per second. This means every two seconds the bucket receives 1 new credit. As such, if your AWS account is making the ListSteps API calls faster than one call per two seconds, you will gradually experience throttled exceptions.

Now in order to avoid this error, increasing the limit could temporarily delay the issue but you might see the same issue again when you hit the increased limits. Hence, the best way to avoid this error is to follow the below recommendation, which can also be found in this [2] blog:

    	- Reduce the frequency of the API calls.
    	- Stagger the intervals of the API calls so that they do not all run at once.
    	- Implement exponential backoff (better with jitter) on making API calls.

Another way of reducing List calls to the service is by making parts of your system that keep polling (that keep invoking ListSteps) the service to instead respond to a cluster's state change. A more comprehensive explanation of this can be found in reference[3][4].

If none of the above solutions help with your use case, one can request a limit increase. 

References:-
[1] https://docs.aws.amazon.com/general/latest/gr/emr.html#limits_emr
[2] https://aws.amazon.com/premiumsupport/knowledge-center/emr-cluster-status-throttling-error/
[3] https://aws.amazon.com/blogs/big-data/respond-to-state-changes-on-amazon-emr-clusters-with-amazon-cloudwatch-events/
[4] https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-manage-cloudwatch-events.html

