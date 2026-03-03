from typing import Protocol

from app.schemas.ugh_user import UghUser, UghCreateUser, UserPwd


class IUserService(Protocol):
    """Interface for user-related operations."""
    def get_all_users(self) -> list[UghUser]:
        """Retrieve all users."""
        raise NotImplementedError

    def get_user_by_id(self, user_id: int) -> UghUser:
        """Retrieve user data by user ID."""
        raise NotImplementedError

    def create_user(self, user_data: UserPwd) -> UserPwd | None:
        """Create a new user with the provided data."""
        raise NotImplementedError

    def update_user(self, user_id: int, user_data: UghCreateUser) -> UghCreateUser:
        """Update an existing user's data by user ID."""
        raise NotImplementedError

    def delete_user(self, user_id: int):
        """Delete a user by user ID."""
        raise NotImplementedError