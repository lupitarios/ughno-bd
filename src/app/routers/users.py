from fastapi import APIRouter

router = APIRouter(tags=["users"] )

@router.get("/users")
def get_users():
    return {"message": "Get all users"}

@router.get("/users/{user_id}")
def get_user(user_id: int):
    return {"message": f"Get user with id {user_id}"}

@router.post("/users")
def create_user():
    return {"message": "Create a new user"}

@router.put("/users/{user_id}")
def update_user(user_id: int):
    return {"message": f"Update user with id {user_id}"}

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    return {"message": f"Delete user with id {user_id}"}