from routes.domain.services import RouteCommand
from routes.domain.entities.RouteId import RouteId
from routes.domain.entities.RouteEntity import RouteEntity
from routes.domain.services.RouteDto import RouteCommand

class RouteMapper:
    @staticmethod
    def to_dto(route_entity: RouteEntity) -> RouteCommand:
        return RouteCommand(
            route_id=str(route_entity.route_id),
            user_id=route_entity.user_id,
            tenant_id=route_entity.tenant_id,
            type=route_entity.type,
            description=route_entity.description,
            date=route_entity.date.isoformat() if route_entity.date else None,
            workplace=route_entity.workplace,
            persons=route_entity.persons,
            activity=route_entity.activity,
            diamond_count=route_entity.diamond_count,
            arrow_count=route_entity.arrow_count,
            sticker_count=route_entity.sticker_count,
            working_hours=route_entity.working_hours
        )

    @staticmethod
    def to_entity(route_command: RouteCommand) -> RouteEntity:
        return RouteEntity(
            route_id=RouteId(route_command.route_id) if route_command.route_id else None,
            user_id=route_command.user_id,
            tenant_id=route_command.tenant_id,
            type=route_command.type,
            description=route_command.description,
            date=route_command.date,
            workplace=route_command.workplace,
            persons=route_command.persons,
            activity=route_command.activity,
            diamond_count=route_command.diamond_count,
            arrow_count=route_command.arrow_count,
            sticker_count=route_command.sticker_count,
            working_hours=route_command.working_hours
        )