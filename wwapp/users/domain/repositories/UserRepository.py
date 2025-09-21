from abc import ABC, abstractmethod

from users.domain.entities.UserEntity import UserEntity


class UserRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id) -> UserEntity:
        pass

    @abstractmethod
    def get_all_users(self) -> list[UserEntity]:
        pass
