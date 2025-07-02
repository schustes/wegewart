from ..usecases.ForReadingUsers import ForReadingUsers
from ..usecases.UserRepository import UserRepository

class UserService(ForReadingUsers):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_all_users(self):
        users = self.user_repository.get_all_users()
        return users

    def get_user_by_id(self, id):
        user = self.user_repository.get_user_by_id(id)
        if not user:
            return None
        return user