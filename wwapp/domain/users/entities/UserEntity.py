#from app.domain.users.entities.UserId import UserId


from .UserId import UserId

class UserEntity:
    def __init__(self, user_id: UserId, name: str, email: str):
        self.name = name
        self.user_id = user_id
        self.email = email

    def __repr__(self):
        return f"UserEntity(user_id={self.user_id}, name={self.name}, email={self.email})"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email
        }
    