class UserDto:

    def __init__(self, user_id: str, first_name: str, last_name: str, email: str, tenant_id: str):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.tenant_id = tenant_id  
