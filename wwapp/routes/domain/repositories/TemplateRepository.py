from abc import ABC, abstractmethod
from routes.domain.entities.RouteEntity import RouteEntity


class TemplateRepository(ABC):
    @abstractmethod
    def get_latest_template(self):
        pass