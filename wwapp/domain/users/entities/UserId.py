import uuid

class UserId:
    def __init__(self, user_id: str):
        if not isinstance(user_id, str):
            raise TypeError("UserId must be a string")
        if not user_id:
            raise ValueError("UserId cannot be empty")
        self._user_id = user_id

    @property
    def value(self) -> str:
        return self._user_id

    @staticmethod
    def generate() -> 'UserId':
        return UserId(str(uuid.uuid4()))
    
    def __str__(self) -> str:
        return self._user_id