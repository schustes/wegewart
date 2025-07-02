import boto3

from users.domain.usecases.UserRepository import UserRepository

class UserDynamoDbRepository(UserRepository):
    def get_dynamodb_client(self):
        client = boto3.resource('dynamodb', 'eu-central-1')
        #print ("====== DynamoDB Client ===")
        #s = client.list_tables()
        #print(s)
        #print ("====== DynamoDB Client ===")
        return client

    def get_all_users(self):
        dynamodb = self.get_dynamodb_client()
        response = dynamodb.meta.client.scan(TableName='UsersTable')
        return response.get('Items', [])

    def get_user_by_id(self, user_id):
        dynamodb = self.get_dynamodb_client()
        response = dynamodb.meta.client.get_item(
            TableName='UsersTable',
            Key={'UserId': user_id}
        )
        return response.get('Item', None)

    def add_user(self, user):
        pass


    def update_user(self, user):
        pass


    def delete_user(self, user_id):
        pass    