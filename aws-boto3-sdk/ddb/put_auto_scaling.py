import boto3
autoscaling_client = boto3.client('application-autoscaling')

percent_of_use_to_aim_for = 50.0
scale_out_cooldown_in_seconds = 60
scale_in_cooldown_in_seconds = 60
autoscaling_client.put_scaling_policy(ServiceNamespace='dynamodb',
                                    ResourceId='table/Test_table1',
                                    PolicyType='TargetTrackingScaling',
                                    PolicyName='ScaleDynamoDBReadCapacityUtilization',
                                    ScalableDimension='dynamodb:table:ReadCapacityUnits',
                                    TargetTrackingScalingPolicyConfiguration={
                                      'TargetValue': percent_of_use_to_aim_for,
                                      'PredefinedMetricSpecification': {
                                        'PredefinedMetricType': 'DynamoDBReadCapacityUtilization'
                                      },
                                      'ScaleOutCooldown': scale_out_cooldown_in_seconds,
                                      'ScaleInCooldown': scale_in_cooldown_in_seconds
                                    })
autoscaling_client.put_scaling_policy(ServiceNamespace='dynamodb',
                                    ResourceId='table/Test_table1',
                                    PolicyType='TargetTrackingScaling',
                                    PolicyName='ScaleDynamoDBWriteCapacityUtilization',
                                    ScalableDimension='dynamodb:table:WriteCapacityUnits',
                                    TargetTrackingScalingPolicyConfiguration={
                                      'TargetValue': percent_of_use_to_aim_for,
                                      'PredefinedMetricSpecification': {
                                        'PredefinedMetricType': 'DynamoDBWriteCapacityUtilization'
                                      },
                                      'ScaleOutCooldown': scale_out_cooldown_in_seconds,
                                      'ScaleInCooldown': scale_in_cooldown_in_seconds
                                    })
