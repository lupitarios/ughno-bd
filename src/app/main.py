from fastapi import FastAPI

from .routers import ai_generative, users

app = FastAPI()

app.include_router(users.router)
app.include_router(ai_generative.router)
@app.get("/")
def read_root():
    return {"message": "Welcome to the UghNo API!"}