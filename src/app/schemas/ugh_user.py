from pydantic import BaseModel, EmailStr

class UghCreateUser(BaseModel):
    name: str
    username: str
    email: EmailStr
    disabled: bool | None = None

    def __str__(self):
        return f"UghUser(name={self.name}, username='{self.username}', email='{self.email}', disabled={self.disabled})"

class UserId(UghCreateUser):
    user_id: int

    def __str__(self):
        return f"User(user_id={self.user_id})"

class UserPwd(UghCreateUser):
    hashed_password: str

class UghUser(UserId, UghCreateUser):
    def __str__(self):
        return f"UghUser(user_id={self.user_id}, name='{self.name}', email='{self.email}')"

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None