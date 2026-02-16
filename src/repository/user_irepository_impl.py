import logging
from typing import List

from repository.db.db_models import User
from repository.user_irepository import IUserRepository
from repository.db.db_configuration import DBConfiguration

logger = logging.getLogger(__name__)

class UserRepositoryImpl(IUserRepository):
    def __init__(self):
        # Initialize database connection or any required resources
        db_configuration = DBConfiguration()
        self.db = db_configuration.db_connection()
        self.session = db_configuration.db_session()

    def get(self, user_id: int) -> User | None:
        # Implement logic to retrieve user data from the database
        try:
            user_by_id = self.session.query(User).get(user_id)
            self.session.commit()
            self.session.close()
            return user_by_id
        except Exception as e:
            self.session.rollback()
            logger.error(e)

    def get_all(self) -> List[User] | None:
        # Implement logic to retrieve all user data from the database
        try:
            all_users = self.session.query(User).all().limit(100)
            self.session.commit()
            self.session.close()
            return all_users
        except Exception as e:
            self.session.rollback()
            logger.error(e)

    def save(self, user: User) -> None:
        try:
            self.session.add(user)
            self.session.commit()
            self.session.close()
            logger.info("User saved successfully.")
        except Exception as e:
            self.session.rollback()
            logger.error(e)

    def delete(self, user_id: int):
        try:
            user_to_delete = self.session.query(User).get(user_id)
            if user_to_delete:
                self.session.delete(user_to_delete)
                self.session.commit()
                logger.info(f"User with id {user_id} deleted successfully.")
            else:
                logger.info(f"User with id {user_id} not found.")
            self.session.close()
        except Exception as e:
            self.session.rollback()
            logger.error(e)

    def update(self, user_id: int, user) -> User | None:
        try:
            user_to_update = self.session.query(User).get(user_id)
            if user_to_update:
                user_to_update.name = user.name
                user_to_update.email = user.email
                self.session.commit()
                logger.info(f"User with id {user_id} updated successfully.")
            else:
                logger.info(f"User with id {user_id} not found.")
            self.session.close()
            return user_to_update
        except Exception as e:
            self.session.rollback()
            logger.error(e)
