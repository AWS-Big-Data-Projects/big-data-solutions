It's hard to come up with exact numbers, because these numbers should be set based on your workloads. So, what I can do is to provide you some numbers to start with, and then you should experiment with these configs and your workloads to fine tune them.

As an example if you have 62G per node you can start with an Xmx of, say 50G, as you should set aside some overhead for the native memory and leave some room for the OS and other daemons running on the machines, if any. In production we use a G1 region size of 32M, which is also the documented value in the deployment docs.

Given that the max heap size is 50G, I think you can start experimenting with the following values and determine the right values for your workloads:

    query.max-memory-per-node = 20GB
    query.max-total-memory-per-node =20GB
    memory.heap-headroom-per-node = 10GB (This is the amount of heap memory to set aside as headroom/buffer (e.g., for untracked allocations)).

With a headroom of 10G and a max total memory per node of 20G the general pool on each worker will be of size 50-10-20 = 20G, and that's 20G*10=200G in the entire cluster. When we determine the query.max-memory (the peak global user memory limit) we also consider the hash partition count (query.initial-hash-partitions configuration, which is the number of partitions for distributed joins and aggregations). 

Assuming you have 10 node cluster, you can set query.initial-hash-partitions to 8, with that if we set query.max-memory to 60G that will result in 60/7.5GB= 8 GB( round-off) per node memory usage roughly (if there is no skew and data is well distributed), and since we have query.max-memory-per-node of 20GB, that means we allow a skew factor of 20/8=2.5=3(round-off) (that is, we allow tasks to consume twice as much memory when the data is not well distributed). Again, you should definitely experiment and tune these values, and figure out what works for you.
