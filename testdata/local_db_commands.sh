aws dynamodb list-tables --endpoint-url http://localhost:8000

aws dynamodb scan --table-name Routes --endpoint-url http://localhost:8000

aws dynamodb delete-item --endpoint-url http://localhost:8000 --table-name UsersTable --key '{"user_id":{"S":"a8954662-6115-4c64-819c-19f68a46cee6"}}'

aws dynamodb put-item --table-name UsersTable --endpoint-url http://localhost:8000 --item file://user_1.json

aws dynamodb delete-table --table-name UsersTable --endpoint-url http://localhost:8000