from users.domain.services import UserMapper
from ...usecases.ForReadingUsers import ForReadingUsers
from users.domain.repositories.UserRepository import UserRepository

class UserService(ForReadingUsers):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_all_users(self):
        userEntities = self.user_repository.get_all_users()
        return [UserMapper.to_dto(user) for user in userEntities]

    def get_user_by_id(self, id):
        userEntity = self.user_repository.get_user_by_id(id)
        if not userEntity:
            return None
        return UserMapper.to_dto(userEntity)
    