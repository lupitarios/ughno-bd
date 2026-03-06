from typing import Protocol, List

from app.schemas.ugh_user import UghUserId, UserPwd
from repository.models.user import User


class IUserRepository(Protocol):
    """Interface for a repository that handles user data repository."""

    def get_by_id(self, user_id: int) -> UghUserId:
        """Retrieve user data from the database."""
        raise NotImplementedError("Method 'get' must be implemented by subclasses")

    def get_by_username(self, username: str) -> UserPwd:
        """Retrieve user data from the database."""
        raise NotImplementedError("Method 'get' must be implemented by subclasses")


    def get_all(self) -> List[UghUserId]:
        """Retrieve all user data from the database."""
        raise NotImplementedError("Method 'get_all' must be implemented by subclasses")

    def save(self, user: User) -> None:
        """Save user data to the database."""
        raise NotImplementedError("Method 'save' must be implemented by subclasses")

    def delete(self, user_id: int) -> UghUserId:
        """Delete user data from the database."""
        raise NotImplementedError("Method 'delete' must be implemented by subclasses")

    def update(self, user_id: int, user: User) -> UghUserId:
        """Update user data in the database."""
        raise NotImplementedError("Method 'update' must be implemented by subclasses")
