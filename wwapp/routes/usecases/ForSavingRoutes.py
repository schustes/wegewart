from abc import ABC, abstractmethod

from routes.domain.services.RouteDto import RouteCommand


class ForSavingRoutes(ABC):
    @abstractmethod
    def add_route(self, route: RouteCommand):
        pass

    @abstractmethod
    def update_route(self, route: RouteCommand):
        pass

    @abstractmethod
    def delete_route(self, route_id: str):
        pass
