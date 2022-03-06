An instance group goes into arrested state if it encounters too many errors while trying to start the newcluster nodes. For example, if new nodes fail while performing bootstrap actions, the instance group goesinto an ARRESTED state, rather than continuously provisioning new nodes. After you resolve the under-lying issue, reset the desired number of nodes on the cluster's instance group, and then the instancegroup resumes allocating nodes. Modifying an instance group instructs Amazon EMR to attempt to provisionnodes again. No running nodes are restarted or terminated.In the AWS CLI, the list-instances subcommand returns all instances and their states as does thedescribe-cluster subcommand. In the Amazon EMR CLI, the --describe command returns all in-stance groups and node types, and you can see the state of the instance groups for the cluster. If AmazonEMR detects a fault with an instance group, it changes the group's state to ARRESTED


To reset a cluster in an ARRESTED state using the AWS CLI•Type the describe-cluster subcommand with the --cluster-id parameter to view the state of the instances in your cluster.

For example, to view information on all instances and instance groups in a cluster, type:

    aws emr describe-cluster --cluster-id j-3KVXXXXXXY7UG

The output will display information about your instance groups and the state of the instances.

To view information on a particular instance group, type the list-instances subcommand withthe --cluster-id and --instance-group-types parameters. You can view information for theMASTER, CORE, or TASK groups:

    aws emr list-instances --cluster-id j-3KVXXXXXXY7UG --instance-group-types"CORE"

Use the modify-instance-groups subcommand with the --instance-groups parameter toreset a cluster in the ARRESTED state. The instance group id is returned by the describe-clustersubcommand:


    aws emr modify-instance-groups --instance-groups InstanceGroupId=string,In stanceCount=integer

Example : 
  
    aws emr modify-instance-groups --instance-groups InstanceGroupId=ig-3SUXXXXXXQ9ZM,InstanceCount=3

Note : You do not need to change the number of nodes from the original configuration to free a runningcluster. Set -–instance-count to the same count as the original setting.

References:

[1] https://docs.aws.amazon.com/cli/latest/reference/emr/modify-instance-groups.html
