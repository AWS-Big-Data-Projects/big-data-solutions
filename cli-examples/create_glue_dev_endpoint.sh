  aws glue create-dev-endpoint --endpoint-name "endpoint1" --role-arn "arn:aws:iam::account-id:role/role-name" --number-of-nodes "3" --glue-version "1.0" --arguments '{"GLUE_PYTHON_VERSION": "3"}' --region "region-name"
