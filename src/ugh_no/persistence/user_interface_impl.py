from src.ugh_no.persistence.user_interface import IUserRepository


class UserRepositoryImpl(IUserRepository):
    def __init__(self):
        # Initialize database connection or any required resources
        pass

    def get(self, user_id: int):
        # Implement logic to retrieve user data from the database
        pass

    def get_all(self):
        # Implement logic to retrieve all user data from the database
        pass

    def save(self, user):
        pass

    def delete(self, user_id: int):
        pass

    def update(self, user_id: int, user):
        pass