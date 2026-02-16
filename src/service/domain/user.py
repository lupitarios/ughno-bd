class User:
    """Represents a user in the system."""

    def __init__(self, user_id: int, username : str,  name: str, email: str):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.email = email

    def __repr__(self):
        return f"User(user_id={self.user_id}, name='{self.name}', email='{self.email}')"

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, value: int):
        if not isinstance(value, int):
            raise ValueError("user_id must be an integer")
        self._user_id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("name must be a string")
        self._name = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if not isinstance(value, str):
            raise ValueError("email must be a string")
        self._email = value
