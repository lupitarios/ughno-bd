from pydantic import BaseModel

# The UghUser class represents a user in the system, containing attributes such as user_id, name, and email.
class UghUser(BaseModel):
    user_id: int
    name: str
    email: str

    def __str__(self):
        return f"UghUser(user_id={self.user_id}, name='{self.name}', email='{self.email}')"