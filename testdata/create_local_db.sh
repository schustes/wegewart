aws dynamodb create-table  --endpoint-url http://localhost:8000 \
    --table-name Users \
    --attribute-definitions AttributeName=user_id,AttributeType=S \
    --key-schema AttributeName=user_id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5   

aws dynamodb create-table  --endpoint-url http://localhost:8000 \
    --table-name Routes \
    --attribute-definitions AttributeName=route_id,AttributeType=S AttributeName=date,AttributeType=S\
    --key-schema AttributeName=route_id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --global-secondary-indexes '[
        {
            "IndexName": "date-index",
            "KeySchema":[{"AttributeName":"date","KeyType":"HASH"}],
            "Projection":{"ProjectionType":"ALL"},
            "ProvisionedThroughput":{"ReadCapacityUnits":5,"WriteCapacityUnits":5}
        }
    ]'

aws dynamodb create-table  --endpoint-url http://localhost:8000 \
    --table-name Routes1 \
    --attribute-definitions AttributeName=route_id,AttributeType=S\
    --key-schema AttributeName=route_id,KeyType=HASH\
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

aws dynamodb create-table  --endpoint-url http://localhost:8000 \
    --table-name Routes2 \
    --attribute-definitions AttributeName=route_id,AttributeType=S AttributeName=date,AttributeType=S\
    --key-schema AttributeName=route_id,KeyType=HASH AttributeName=date,KeyType=RANGE\
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5