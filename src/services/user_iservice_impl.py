import logging
from app import security
from app.schemas.ugh_user import UghUser, UghCreateUser, UserPwd
from repository.models.user import User
from repository.user_irepository_impl import UserRepositoryImpl
from services.user_iservice import  IUserService

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UserServiceImpl(IUserService):
    def __init__(self, user_repository: UserRepositoryImpl):
        self.user_repository = user_repository

    def get_user_by_id(self, user_id: int) -> UghUser | None:
        logger.debug(f"Getting user with id: {user_id}")
        user_found = self.user_repository.get(user_id)
        return UghUser(user_id=user_found.user_id,
                       name=user_found.name,
                       username=user_found.username ,
                       email=user_found.email,
                       disabled=user_found.disabled) if user_found else None

    def get_all_users(self) -> list[UghUser] | None:
        logger.debug("Getting all users")
        list_users_found = self.user_repository.get_all()
        logger.debug(f"Service List of users found: {list_users_found}")
        return list_users_found

    def create_user(self, user_data: UserPwd) -> UserPwd | None:
        print(f"Creating user: {user_data}")
        user = User()
        user.name = user_data.name
        user.email = user_data.email
        user.username = user_data.username
        user.disabled = user_data.disabled

        try:
            print(f"User to create: {user} to hash password: {user_data.hashed_password}")
            hashed_password = security.get_password_hash(user_data.hashed_password)
            user.hashed_password = hashed_password

            self.user_repository.save(user)
            print("User created successfully")
            return user_data
        except Exception as e:
            print(f"Service Error creating user: {e}")

    def delete_user(self, user_id: int):
        logger.debug(f"Deleting user with id: {user_id}")
        self.user_repository.delete(user_id)

    def update_user(self, user_id: int, user_data: UghCreateUser) -> UghUser | None:
        logger.debug(f" Service Updating user with id: {user_id} to new values: {user_data}")
        user_to_update = User()
        user_to_update.name = user_data.name
        user_to_update.username = user_data.username
        user_to_update.email = user_data.email
        user_to_update.disabled = user_data.disabled
        logger.info("User to update created successfully")
        return self.user_repository.update(user_id, user_to_update)