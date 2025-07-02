from abc import ABC, abstractmethod

class ForReadingUsers(ABC):

    @abstractmethod
    def get_user_by_id(self, user_id):
        pass

    @abstractmethod
    def get_all_users(self):
        pass