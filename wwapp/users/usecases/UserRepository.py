from abc import ABC, abstractmethod


class UserRepository(ABC):
    @abstractmethod
    def add_user(self, user):
        """Add a new user to the repository."""
        pass

    @abstractmethod
    def update_user(self, user):
        """Update an existing user in the repository."""
        pass

    @abstractmethod
    def delete_user(self, user_id):
        """Delete a user from the repository."""
        pass

    @abstractmethod
    def get_user_by_id(self, user_id):
        """Retrieve a user by their ID."""
        pass

    @abstractmethod
    def get_all_users(self):
        """Retrieve all users from the repository."""
        pass