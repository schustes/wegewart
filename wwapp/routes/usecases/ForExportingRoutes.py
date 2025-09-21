from abc import ABC, abstractmethod

from routes.domain.entities.RouteEntity import RouteEntity


class ForExportingRoutes(ABC):
    @abstractmethod
    def export(self, year: int) -> bytes:  
        pass
