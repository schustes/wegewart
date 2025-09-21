from users.domain.entities.UserEntity import UserEntity
from users.domain.entities.UserId import UserId
from .UserDto import UserDto

@staticmethod
def to_dto(user_entity: UserEntity) -> UserEntity:
        return UserEntity(
            user_id=str(user_entity.user_id),
            first_name=user_entity.first_name,
            last_name=user_entity.last_name,
            email=user_entity.email,
            tenant_id=user_entity.tenant_id
        )   
@staticmethod
def to_entity(user_dto: UserEntity) -> UserEntity:
        return UserEntity( 
            user_id=UserId(user_dto.user_id),
            email=user_dto.email,
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            tenant_id=user_dto.tenant_id
        )    