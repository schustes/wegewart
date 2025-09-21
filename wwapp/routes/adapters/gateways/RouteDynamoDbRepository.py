from datetime import datetime
from decimal import Decimal
import boto3
from flask import session

from routes.domain.entities.RouteId import RouteId
from routes.domain.entities.RouteEntity import RouteEntity
from routes.domain.repositories.RouteRepository import RouteRepository
from settings import DYNAMODB

class RouteDynamoDbRepository(RouteRepository):
    def get_dynamodb_client(self):
        client = boto3.resource('dynamodb', 
                                region_name=DYNAMODB.get("REGION"), 
                                endpoint_url=DYNAMODB.get("ENDPOINT_URL")
                                )
        return client

    def get_all_routes(self):
        dynamodb = self.get_dynamodb_client()

        table = dynamodb.Table('Routes')
        tenant_id = session.get('tenant_id')
        
        response = table.scan(
            FilterExpression="tenant_id = :tenant_id_val",
            IndexName='date-index',
            ExpressionAttributeValues={
                ":tenant_id_val": tenant_id,
            }
        )

        dict_items = response.get('Items', [])        

        route_entities = []
        for item in dict_items:
            route_entity = self.mapFromDict(item)
            route_entities.append(route_entity)

        route_entities.reverse()
        return route_entities

    def get_all_routes_of_year(self, year: int):
        dynamodb = self.get_dynamodb_client()

        table = dynamodb.Table('Routes')
        tenant_id = session.get('tenant_id')
        start_date = datetime(year-1, 12, 31)
        end_date = datetime(year, 12, 31)
        start_date_str = start_date.isoformat()
        end_date_str = end_date.isoformat()

        response = table.scan(
            FilterExpression="tenant_id = :tenant_id_val AND #d BETWEEN :start_date AND :end_date",
            IndexName='date-index',
            #ScanIndexForward=True,
            ExpressionAttributeValues={
                ":tenant_id_val": tenant_id,
                ":start_date": start_date_str,
                ":end_date": end_date_str
            },
            ExpressionAttributeNames={
                '#d': 'date'
            }            
        )

        dict_items = response.get('Items', [])        

        return self.map_to_entity_list(dict_items)

    def get_my_routes(self):
        dynamodb = self.get_dynamodb_client()

        table = dynamodb.Table('Routes')
        tenant_id = session.get('tenant_id')
        user_id = session.get('user_id')
        
        response = table.scan(
            FilterExpression="tenant_id = :tenant_id_val AND user_id = :user_id_val",
            IndexName='date-index',
            ExpressionAttributeValues={
                ":tenant_id_val": tenant_id,
                ":user_id_val": user_id
            }
        )
        dict_items = response.get('Items', [])        

        route_entities =  self.map_to_entity_list(dict_items)
        route_entities.reverse()
        return route_entities
    
    def get_route_by_id0(self, route_id, date=None):
        dynamodb = self.get_dynamodb_client()
        table = dynamodb.Table('Routes')
        key_condition = "route_id = :route_id_val"
        
        expression_values = {":route_id_val": route_id}
        response = table.query(
            KeyConditionExpression=key_condition,
            ExpressionAttributeValues=expression_values
        )
        items = response.get('Items', [])
        if items:
            return self.mapFromDict(items[0])
        return None

    def get_route_by_id(self, id: RouteId) -> RouteEntity | None:
        dynamodb = self.get_dynamodb_client()
        response = dynamodb.meta.client.get_item(
            TableName='Routes',
            Key={
                    'route_id': id.value
                }
        )        
        item = response.get('Item', None)
        if (item is not None): 
            return self.mapFromDict(item)
        return None

    def add_route(self, routeEntity):
        print("RouteEntity to add:", routeEntity)
        dynamodb = self.get_dynamodb_client()
        table = dynamodb.Table('Routes')
        item = {
            'route_id': str(routeEntity.route_id),
            'user_id': routeEntity.user_id,
            'tenant_id': routeEntity.tenant_id,
            'type': routeEntity.type,
            'description': routeEntity.description,
            'date': routeEntity.date.strftime("%Y-%m-%d") if routeEntity.date else None,
            'workplace': routeEntity.workplace,
            'persons': routeEntity.persons,
            'activity': routeEntity.activity,
            'diamond_count': int(routeEntity.diamond_count) if routeEntity.diamond_count is not None else 0,
            'arrow_count': int(routeEntity.arrow_count) if routeEntity.arrow_count is not None else 0,
            'sticker_count': int(routeEntity.sticker_count) if routeEntity.sticker_count is not None else 0,
            'working_hours': Decimal(str(routeEntity.working_hours)) if routeEntity.working_hours is not None else 0.0
        }
        # Remove None values to avoid DynamoDB errors
        # TODO proper integrity checks to avoid this
        item = {k: v for k, v in item.items() if v is not None}
        table.put_item(Item=item)
    
    def update_route(self, routeEntity):
        dynamodb = self.get_dynamodb_client()
        table = dynamodb.Table('Routes')
        print("RouteEntity to update:", routeEntity.route_id)
        table.update_item(
            Key={'route_id': str(routeEntity.route_id)},
            UpdateExpression="""
                SET description = :description,
                    workplace = :workplace,
                    persons = :persons,
                    activity = :activity,
                    diamond_count = :diamond_count,
                    arrow_count = :arrow_count,
                    sticker_count = :sticker_count,
                    working_hours = :working_hours,
                    #t = :type,
                    #d = :date
            """,
            ExpressionAttributeValues={
                ':type': routeEntity.type,
                ':description': routeEntity.description,
                ':date': routeEntity.date.strftime("%Y-%m-%d") if routeEntity.date else None,
                ':workplace': routeEntity.workplace,
                ':persons': routeEntity.persons,
                ':activity': routeEntity.activity,
                ':diamond_count': int(routeEntity.diamond_count) if routeEntity.diamond_count is not None else 0,
                ':arrow_count': int(routeEntity.arrow_count) if routeEntity.arrow_count is not None else 0,
                ':sticker_count': int(routeEntity.sticker_count) if routeEntity.sticker_count is not None else 0,
                ':working_hours': Decimal(str(routeEntity.working_hours)) if routeEntity.working_hours is not None else 0.0
            },
            ExpressionAttributeNames={
                '#t': 'type',
                '#d': 'date'
            }
        )

    def delete_route(self, route_id):
        dynamodb = self.get_dynamodb_client()
        table = dynamodb.Table('Routes')
        table.delete_item(
            Key={
                'route_id': route_id
            }
        )

    def mapFromDict(self, item):
        date_value = item.get('date')
        date_obj = None
        if date_value:
            try:
                date_obj = datetime.strptime(date_value, "%Y-%m-%d").date()
            except Exception:
                date_obj = None
        return RouteEntity(
            route_id = RouteId(item.get('route_id')),
            user_id = item.get('user_id'),
            tenant_id = item.get('tenant_id'),
            type = item.get('type'),
            description = item.get('description'),
            date = date_obj,
            workplace = item.get('workplace', ""),
            persons = item.get('persons', ""),
            activity = item.get('activity', ""),
            diamond_count = int(item.get('diamond_count', 0)),
            arrow_count = int(item.get('arrow_count', 0)),
            sticker_count = int(item.get('sticker_count', 0)),
            working_hours = float(item.get('working_hours', 0.0))
        )

    def map_to_entity_list(self, dict_items):
        route_entities = []
        for item in dict_items:
            route_entity = self.mapFromDict(item)
            route_entities.append(route_entity)

        return route_entities
