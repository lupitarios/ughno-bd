from typing import Protocol, List

from src.ugh_no.persistence.domain.user import User


class IUserRepository(Protocol):
    """Interface for a repository that handles user data persistence."""

    def get(self, user_id: int) -> User:
        """Retrieve user data from the database."""
        raise NotImplementedError("Method 'get' must be implemented by subclasses")

    def get_all(self) -> List[User]:
        """Retrieve all user data from the database."""
        raise NotImplementedError("Method 'get_all' must be implemented by subclasses")

    def save(self, user: User) -> None:
        """Save user data to the database."""
        raise NotImplementedError("Method 'save' must be implemented by subclasses")

    def delete(self, user_id: int) -> User:
        """Delete user data from the database."""
        raise NotImplementedError("Method 'delete' must be implemented by subclasses")

    def update(self, user_id: int, user: User) -> User:
        """Update user data in the database."""
        raise NotImplementedError("Method 'update' must be implemented by subclasses") 
