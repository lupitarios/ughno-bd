import os
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import ai_generative, users
app = FastAPI()

app.include_router(users.router)
app.include_router(ai_generative.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

@app.get("/")
def read_root():
    return {"message": "Welcome to the UghNo API!"}

if __name__ == '__main__':
    uvicorn.run("app:app",host=os.environ.get("HOST"), port=int(os.environ.get("PORT")), reload=True)