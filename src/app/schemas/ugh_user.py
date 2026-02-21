from pydantic import BaseModel, EmailStr

class UserId(BaseModel):
    user_id: int

    def __str__(self):
        return f"User(user_id={self.user_id})"

class UghCreateUser(BaseModel):
    name: str
    username: str
    email: EmailStr

    def __str__(self):
        return f"UghUser(name={self.name}, username='{self.username}', email='{self.email}')"

class UghUser(UserId, UghCreateUser):
    def __str__(self):
        return f"UghUser(user_id={self.user_id}, name='{self.name}', email='{self.email}')"