from typing import List

from src.ugh_no.persistence.domain.user import User

def get(self, user_id: int) -> User:
    # Implement logic to retrieve user data from the database
    pass

def get_all(self) -> List[User]:
    # Implement logic to retrieve all user data from the database
    pass

def save(self, user: User) -> None:
    pass

def delete(self, user_id: int) -> User:
    pass

def update(self, user_id: int, user: User) -> User:
    pass