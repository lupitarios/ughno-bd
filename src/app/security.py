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

from app.schemas.ugh_user import UserPwd, User


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str]  = []

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token",
                                     scopes={"admin": "Read all items. Update/Write items. Delete items.",
                                             "user": "Read items. Update/Write items.",
                                             "read-only": "Read items."})
fake_users_db = {}

load_dotenv()
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

# For the sake of this example, the users will be stored in a dictionary.
# In production, you would use a database to store users and their hashed passwords.
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserPwd(**user_dict)

def authenticate_user(fake_users_db, username: str, password: str):
    user = get_user(fake_users_db, username)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

async def get_current_user(security_scopes: SecurityScopes , token: Annotated[str, Depends(oauth2_scheme)]):

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
        token_scopes = scope.split(" ")
        token_data = TokenData(scopes=token_scopes , username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)
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

async def get_current_active_user(current_user: Annotated[User, Security(get_current_user, scopes=["me"])]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user