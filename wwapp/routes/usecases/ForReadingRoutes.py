from abc import ABC, abstractmethod

from routes.domain.services.RouteDto import RouteCommand

class ForReadingRoutes(ABC):

    @abstractmethod
    def get_route_by_id(self, route_id) -> RouteCommand :
        pass

    @abstractmethod
    def get_all_routes(self) -> list[RouteCommand]:
        pass

    @abstractmethod
    def get_my_routes(self) -> list[RouteCommand]:
        pass

