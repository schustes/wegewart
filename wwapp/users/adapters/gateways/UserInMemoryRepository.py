import sqlite3
from users.domain.entities.UserEntity import UserEntity
from users.domain.entities.UserId import UserId
from users.usecases.UserRepository import UserRepository

class UserInMemoryRepository(UserRepository):
    def __init__(self, connection):
        self.db = None
        self.connection = connection

    def add_user(self, user: UserEntity) -> UserEntity:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user: UserEntity) -> UserEntity:
        existing_user = self.get_user_by_id(user.id)
        if existing_user:
            existing_user.name = user.name
            existing_user.email = user.email
            self.db.commit()
            self.db.refresh(existing_user)
            return existing_user
        return None

    def delete_user(self, user_id: int) -> None:
        user = self.get_user_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()

    def get_user_by_id(self, user_id):
        if (user_id == "id-1"): 
           return UserEntity(UserId.generate(), "John Doe", "mail")
        else: 
             return UserEntity(UserId.generate(), "Stephan", "mail")
        
        #return UserAggregate(UserEntity("id-1", "John Doe", "mail"))

    def get_all_users(self):
        return [UserEntity(UserId.generate(), "John Doe", "mail"), UserEntity(UserId.generate(), "Stephan", "mail")]
        #return [UserAggregate(UserEntity("id-1", "John Doe", "mail")), UserAggregate(UserEntity("id-2", "Stephan", "mail"))]              