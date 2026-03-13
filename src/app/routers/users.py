from datetime import timedelta
from typing import Annotated

import uvicorn
import logging

from fastapi import APIRouter, HTTPException, Security, Depends
from fastapi.security import (OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes)

from app import security
from app.schemas.ugh_user import UghUserId, UghCreateUser, UserPwd
from repository.user_irepository_impl import UserRepositoryImpl
from services.user_iservice_impl import UserServiceImpl
import app.security as auth

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router = APIRouter(tags=["users"] )
user_service = UserServiceImpl(UserRepositoryImpl())

@router.get("/users", dependencies=[Security(security.get_current_active_user, scopes=["user:read"])])
def get_users()-> list[UghUserId] | None:
    logger.info('Get All Users')
    return user_service.get_all_users()

@router.get("/users/{user_id}", dependencies=[Security(security.get_current_active_user, scopes=["user:read"])])
def get_user(user_id: int)->UghUserId:
    logger.info(f"Get user with id {user_id}")
    user_found = user_service.get_user_by_id(user_id)
    if user_found:
        return user_found
    else:
        logger.info(f"User with id {user_id} not found")
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

@router.post("/users", dependencies=[Security(security.get_current_active_user, scopes=["user:write"])])
def create_user(request: UserPwd)->UserPwd:
    logger.debug(f"Create a new user with request: {request}")
    try:
        return user_service.create_user(request)
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=400, detail="An Error occurred creating user")

@router.put("/users/{user_id}", dependencies=[Security(security.get_current_active_user, scopes=["user:write"])])
def update_user(user_id: int, request: UghCreateUser)->UghUserId:
    logger.info(f"Update user with id {user_id}")
    try:
        return user_service.update_user(user_id, request)
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        raise HTTPException(status_code=400, detail="An Error occurred while updating user")

@router.delete("/users/{user_id}", dependencies=[Security(security.get_current_active_user, scopes=["admin:delete"])])
def delete_user(user_id: int) -> dict:
    logger.debug(f"Delete user with id {user_id}")
    try:
        user_service.delete_user(user_id)
        return {"message": f"User with id {user_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        raise HTTPException(status_code=400, detail="An Error occurred deleting user")

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> auth.Token:
    user_found_db = user_service.get_user_by_username(form_data.username)
    logger.debug("User found in DB:", user_found_db)
    user = auth.authenticate_user(user_found_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=security.token_expire_minutes)

    access_token = auth.create_access_token(
        data={"sub": user.username, "scope": " ".join(form_data.scopes)},
        expires_delta=access_token_expires
    )
    return auth.Token(access_token=access_token, token_type="bearer")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0", port=8000, reload=True    )