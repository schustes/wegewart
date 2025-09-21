from users.domain.services.UserDto import UserDto


@staticmethod
def from_user_dto_to_dict(user_dto):
        return {
            "user_id": user_dto.user_id,
            "first_name": user_dto.first_name,
            "last_name": user_dto.last_name,
            "email": user_dto.email,
            "tenant_id": user_dto.tenant_id
        }