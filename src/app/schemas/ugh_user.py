from pydantic import BaseModel, EmailStr

class UghCreateUser(BaseModel):
    name: str
    username: str
    email: EmailStr
    disabled: bool | None = None

    def __str__(self):
        return f"UghUser(name={self.name}, username='{self.username}', email='{self.email}', disabled={self.disabled})"

class UghUserId(UghCreateUser):
    user_id: int

    def __str__(self):
        return f"User(user_id={self.user_id}, name={self.name}, username='{self.username}', email='{self.email}', disabled={self.disabled})"

class UserPwd(UghUserId):
    hashed_password: str