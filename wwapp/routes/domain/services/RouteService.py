from flask import session
from routes.domain.entities.RouteId import RouteId
from routes.domain.repositories.RouteRepository import RouteRepository
from routes.domain.services.RouteMapper import RouteMapper
from routes.usecases.ForReadingRoutes import ForReadingRoutes
from routes.usecases.ForSavingRoutes import ForSavingRoutes

class RouteService(ForReadingRoutes, ForSavingRoutes):
    def __init__(self, route_repository: RouteRepository):
        self.route_repository = route_repository

    def get_all_routes(self):
        routes = self.route_repository.get_all_routes()
        return [RouteMapper.to_dto(route) for route in routes]

    def get_my_routes(self):
        routes = self.route_repository.get_my_routes()
        return [RouteMapper.to_dto(route) for route in routes]

    def get_route_by_id(self, id):
        route = self.route_repository.get_route_by_id(id)
        if not route:
            return None
        return route
    
    def add_route(self, routeCommand):
        self.route_repository.add_route(RouteMapper.to_entity(routeCommand))

    def update_route(self, routeCommand):
        route_entity = RouteMapper.to_entity(routeCommand)
        self.route_repository.update_route(route_entity)
        return RouteMapper.to_dto(self.route_repository.get_route_by_id(route_entity.route_id))

    def delete_route(self, route_id):
        self.route_repository.delete_route(route_id)
