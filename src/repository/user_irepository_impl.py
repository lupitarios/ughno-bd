import logging
from typing import List

from app.schemas.ugh_user import UghUserId
from repository.models.user import User
from repository.user_irepository import IUserRepository
from repository.db_configuration import DBConfiguration

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UserRepositoryImpl(IUserRepository):
    def __init__(self):
        # Initialize database connection or any required resources
        db_configuration = DBConfiguration()
        self.db = db_configuration.create_engine()
        self.session = db_configuration.get_db_session()

    def get(self, user_id: int) -> UghUserId | None:
        # Implement logic to retrieve user data from the database
        try:
            if not self.session.is_active:
                self.session = DBConfiguration().get_db_session()

            user_by_id = self.session.query(User).get(user_id)
            self.session.commit()

            user_converted_found = UghUserId(user_id=user_by_id.user_id,
                                             name=user_by_id.name,
                                             username=user_by_id.username,
                                             email=user_by_id.email,
                                             disabled=user_by_id.disabled) \
                if user_by_id else None

            logger.info(f"Service user found: {user_converted_found}")
            return user_converted_found
        except Exception as e:
            self.session.rollback()
            logger.error(e)
        finally:
            logger.debug("Closing session.")
            if self.session.is_active:
                self.session.close()

    def get_all(self) -> List[UghUserId] | None:
        # Implement logic to retrieve all user data from the database
        try:
            logger.debug(f"Session active:{self.session.is_active}" )
            if self.session._close_state.CLOSED:
                self.session = DBConfiguration().get_db_session()

            all_users = self.session.query(User).all() #.limit(100)
            logger.debug(f"Number of users retrieved: {len(all_users)}" )
            self.session.commit()
            logger.debug("Session committed successfully.")
            list_converted_found = [
                UghUserId(user_id=user.user_id,
                          name=user.name,
                          username=user.username,
                          email=user.email,
                          disabled=user.disabled)
                for user in all_users] if all_users else None
            return list_converted_found
        except Exception as e:
            self.session.rollback()
            logger.error(e)
        finally:
            logger.debug("Closing session.")
            if self.session.is_active:
                self.session.close()

    def save(self, user: User) -> None:
        try:
            if not self.session.is_active:
                self.session = DBConfiguration().get_db_session()
            print("Repo Saving user:", user)
            print(user.__repr__())
            self.session.add(user)
            self.session.commit()
            print("User saved successfully.")
        except Exception as e:
            self.session.rollback()
            print(f"Error saving user, rolling back transaction. {e}")
        finally:
            print("Closing session.")
            if self.session.is_active:
                self.session.close()

    def delete(self, user_id: int):
        try:
            if not self.session.is_active:
                self.session = DBConfiguration().get_db_session()

            user_to_delete = self.session.query(User).get(user_id)
            if user_to_delete:
                self.session.delete(user_to_delete)
                self.session.commit()
                logger.info(f"User with id {user_id} deleted successfully.")
            else:
                logger.info(f"User with id {user_id} not found.")
        except Exception as e:
            self.session.rollback()
            logger.error(e)
        finally:
            logger.debug("Closing session.")
            if self.session.is_active:
                self.session.close()

    def update(self, user_id: int, user: User) -> UghUserId | None:
        try:
            if not self.session.is_active:
                self.session = DBConfiguration().get_db_session()

            logger.debug(f"Updating user with id:{user_id}" )
            user_to_update = self.session.query(User).get(user_id)
            logger.debug(f"User to update: {user_to_update} found in database.")
            if user_to_update:
                user_to_update.name = user.name
                user_to_update.email = user.email
                user_to_update.username = user.username
                user_to_update.disabled = user.disabled
                self.session.commit()
                logger.info(f"User with id {user_id} updated successfully.")
            else:
                logger.info(f"User with id {user_id} not found.")
                return None

            user_converted_updated = UghUserId(
                user_id=user_id,
                name=user.name,
                username=user.username,
                email=user.email,
                disabled=user.disabled)
            logger.debug(f"Service user updated: {user_converted_updated}")
            return user_converted_updated
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error updating user, rolling back transaction. {e}")
        finally:
            logger.debug("Closing session.")
            if self.session.is_active:
                self.session.close()
