aws glue  update-crawler --name ulap-glue-crawler-typeahead --targets '{\"DynamoDBTargets\": [{\"Path\": \"ulap-uat-typeahead\",\"scanAll\": false,\"scanRate\": 1}]}'
