[{
              "Classification": "presto-config",
              "Properties": {
                  "query.max-memory": "8000MB",
                  "query.max-memory-per-node": "30G",
                  "query.max-total-memory-per-node": "40G",
                  "memory.heap-headroom-per-node": "20G",
                  "query.initial-hash-partitions": "20"
              },
              "Configurations": []
          }]

https://github.com/prestodb/presto/issues/11005



To give you more detailed answer here are the memory management properties [1]: 

query.max-memory : 

      This is the max amount of user memory a query can use across the entire cluster. User memory is allocated during execution for things that are directly attributable to or controllable by a user query. For example, memory used by the hash tables built during execution, memory used during sorting, etc. When the user memory allocation of a query across all workers hits this limit it will be killed.

query.max-memory-per-node : 

      This is the max amount of user memory a query can use on a worker. User memory is allocated during execution for things that are directly attributable to or controllable by a user query. For example, memory used by the hash tables built during execution, memory used during sorting, etc. When the user memory allocation of a query on any worker hits this limit it will be killed.

There is one more param i.e. "query.max-total-memory-per-node"

query.max-total-memory-per-node : 

      This is the max amount of user and system memory a query can use on a worker. System memory is allocated during execution for things that are not directly attributable to or controllable by a user query. For example, memory allocated by the readers, writers, network buffers, etc. When the sum of the user and system memory allocated by a query on any worker hits this limit it will be killed. The value of query.max-total-memory-per-node must be greater than query.max-memory-per-node.This config. must be greater than or equal to query.max-memory-per-node (which is only the user memory). The default value of query.max-total-memory-per-node is 30% of the heap size.


query.max-total-memory:

      This is the max amount of user and system memory a query can use across the entire cluster. System memory is allocated during execution for things that are not directly attributable to or controllable by a user query. For example, memory allocated by the readers, writers, network buffers, etc. When the sum of the user and system memory allocated by a query across all workers hits this limit it will be killed. The value of query.max-total-memory must be greater than query.max-memory.

Reference :

[1] https://prestodb.io/docs/current/admin/properties.html#general-properties
