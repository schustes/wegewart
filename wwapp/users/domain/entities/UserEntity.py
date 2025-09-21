#from app.domain.users.entities.UserId import UserId


from .UserId import UserId

class UserEntity:
    def __init__(self, user_id: UserId, first_name: str, last_name: str, email: str, tenant_id: str):
        self.first_name  = first_name
        self.last_name = last_name
        self.user_id = user_id
        self.email = email
        self.tenant_id = tenant_id

    def __repr__(self):
        return f"UserEntity(user_id={self.user_id}, name={self.last_name}, email={self.email})"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "tenant_id": self.tenant_id
        }
    