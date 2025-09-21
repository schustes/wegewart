    
from datetime import datetime
from routes.domain.services.RouteCommand import RouteCommand
from routes.domain.services.RouteDto import RouteCommand

@staticmethod
def route_dto_to_dict(route_dto: 'RouteCommand') -> dict:
        return {
            "route_id": route_dto.route_id,
            "user_id": route_dto.user_id,
            "tenant_id": route_dto.tenant_id,
            "description": route_dto.description,
            "date": route_dto.date,
            "type": route_dto.type,
            "workplace": route_dto.workplace,
            "persons": route_dto.persons,
            "activity": route_dto.activity,
            "diamond_count" : route_dto.diamond_count,
            "arrow_count": route_dto.arrow_count,
            "sticker_count": route_dto.sticker_count,
            "working_hours": route_dto.working_hours
        }
@staticmethod
def route_command_from_dict(data: dict):
        return RouteCommand(
            description=data.get("description", ""),
            date=datetime.strptime(data.get("date", ""), "%Y-%m-%d").date() if data.get("date") else None,
            type=data.get("type", ""),
            workplace=data.get("workplace", ""),
            persons=data.get("persons", ""),
            activity=data.get("activity", ""),
            diamond_count=int(data.get("diamond_count", 0)),
            arrow_count=int(data.get("arrow_count", 0)),
            sticker_count=int(data.get("sticker_count", 0)),
            working_hours=float(data.get("working_hours", 0.0)),
            user_id=None,
            tenant_id=None,
            route_id=data.get("route_id", None)
   )