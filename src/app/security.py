import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, APIRouter, HTTPException, status, Security
from fastapi.security import (OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes)
from pydantic import BaseModel, ValidationError
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from dotenv import load_dotenv
import os
from app.schemas.ugh_user import UserPwd, UghUserId
from repository.user_irepository_impl import UserRepositoryImpl

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str]  = []

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token",
                                     scopes={"admin": "Admin privileges",
                                             "user": "User privileges",
                                             "read-only": "Read items."})

load_dotenv()
logger.info("Environment variables loaded successfully.")
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
dummy_password = os.getenv("DUMMY_PASSWORD")
print("ENV algorithm:", algorithm)

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash(dummy_password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

def authenticate_user(user_in_db, username: str, password: str):
    logger.info(f"Authenticate_user Username: {username}")
    logger.info(f"User found: {user_in_db}")
    if not user_in_db:
        # To mitigate timing attacks, we verify the password against a dummy hash even if the user doesn't exist.
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user_in_db.hashed_password):
        return False
    return user_in_db


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    logger.info(f"create_access_token: {data}")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

async def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]):
        logger.info("get_current_user called with token: %s and security scopes: %s", token, security_scopes.scopes)
        print("get_current_user called with token: %s and security scopes: %s", token, security_scopes.scopes)
        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = f"Bearer"
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            print("Decoded JWT payload:", payload)
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            scope: str = payload.get("scope", "")
            print("Scope from JWT payload:", scope)
            token_scopes = scope.split(" ")
            token_data = TokenData(scopes=token_scopes, username=username)
        except (InvalidTokenError, ValidationError):
            raise credentials_exception

        user_repository = UserRepositoryImpl()
        user = user_repository.get_by_username(username=token_data.username)
        print("User retrieved from database:", user)
        if user is None:
            raise credentials_exception
        for scope in security_scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
        return user

async def get_current_active_user(current_user: Annotated[UghUserId, Security(get_current_user, scopes=["user"])]):
        logger.info(f"get_current_active_user: {current_user}")
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user