#aws dynamodb put-item --table-name UsersTable --endpoint-url http://localhost:8000 --item file://user_1.json
#aws dynamodb put-item --table-name UsersTable --endpoint-url http://localhost:8000 --item file://user_2.json

aws dynamodb put-item --table-name Routes --endpoint-url http://localhost:8000 --item file://route_1.json