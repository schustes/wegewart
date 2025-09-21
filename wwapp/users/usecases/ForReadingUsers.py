from abc import ABC, abstractmethod

from users.domain.services.UserDto import UserDto

class ForReadingUsers(ABC):

    @abstractmethod
    def get_user_by_id(self, user_id) -> UserDto:
        pass

    @abstractmethod
    def get_all_users(self) -> list[UserDto]:
        pass
