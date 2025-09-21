import boto3
from flask import session

from users.domain.entities.UserEntity import UserEntity
from settings import DYNAMODB
from users.domain.repositories.UserRepository import UserRepository

class UserDynamoDbRepository (UserRepository):
    def get_dynamodb_client(self):
        
        client = boto3.resource('dynamodb', 
                                region_name=DYNAMODB.get("REGION"), 
                                endpoint_url=DYNAMODB.get("ENDPOINT_URL"))
        return client

    def get_all_users(self):
        dynamodb = self.get_dynamodb_client()
        table = dynamodb.Table('Users')
        tenant_id = session.get('tenant_id')
        
        response = table.scan(
            FilterExpression="tenant_id = :tenant_id_val",
            ExpressionAttributeValues={
                ":tenant_id_val": tenant_id
            }
        )
        
        dict_items = response.get('Items', [])        

        user_entities = []
        for item in dict_items:
            user_entity = UserEntity(
                user_id = item.get('user_id'),
                first_name=item.get('first_name'),
                last_name=item.get('last_name'),
                email=item.get('email'),
                tenant_id=item.get('tenant_id')
            )
            user_entities.append(user_entity)

        return user_entities

    def get_user_by_id(self, user_id):
        dynamodb = self.get_dynamodb_client()
        response = dynamodb.meta.client.get_item(
            TableName='Users',
            Key={'user_id': user_id}
        )        
        item = response.get('Item', None)
        if (item is not None): 
            user_entity = UserEntity(
            user_id = item.get('user_id'),
            first_name=item.get('first_name'),
            last_name=item.get('last_name'),
            email=item.get('email'),
            tenant_id=item.get('tenant_id')
            )
            return user_entity

        return None
