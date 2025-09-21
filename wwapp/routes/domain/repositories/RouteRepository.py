from abc import ABC, abstractmethod
from routes.domain.entities.RouteEntity import RouteEntity


class RouteRepository(ABC):
    @abstractmethod
    def add_route(self, route):
        pass

    @abstractmethod
    def update_route(self, route):
        pass

    @abstractmethod
    def delete_route(self, route_id):
        pass

    @abstractmethod
    def get_route_by_id(self, route_id) -> RouteEntity:
        pass

    @abstractmethod
    def get_all_routes(self) -> list[RouteEntity]:
        pass

    @abstractmethod
    def get_all_routes_of_year(year: int) -> list[RouteEntity]:
        pass

    @abstractmethod
    def get_my_routes(self) -> list[RouteEntity]:
        pass    