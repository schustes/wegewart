import uuid

class RouteId:
    def __init__(self, route_id: str):
        if not isinstance(route_id, str):
            raise TypeError("RouteId must be a string")
        if not route_id:
            raise ValueError("RouteId cannot be empty")
        self._route_id = route_id

    @property
    def as_str(self) -> str:
        return self._route_id

    @property
    def value(self) -> str:
        return self._route_id

    @staticmethod
    def generate() -> 'RouteId':
        return RouteId(str(uuid.uuid4()))
    
    def __str__(self) -> str:
        return self._route_id