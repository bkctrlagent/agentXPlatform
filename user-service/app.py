from fastapi import FastAPI
from consul import Consul
import uvicorn
from models.User import User
from extensions.ext_db import get_db
from pydantic import BaseModel

class UserRequest(BaseModel):
    name: str
    email: str
    password: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/users")
async def create_user(user: UserRequest):
    db = next(get_db())
    user = User(
        name=user.name,
        email=user.email,
        password=user.password
    )
    db.add(user)
    db.commit()
    return user

@app.get("/users")
async def get_users():
    db = next(get_db())
    users = db.query(User).all()
    return users

def register():
    consul = Consul(host='consul', port=8500)
    consul.agent.service.register(
        name="user-service",
        service_id="user-service-1",
        address="127.0.0.1",
        port=8000,
        tags=["user-service"],
    )


if __name__ == "__main__":
    register()
    uvicorn.run(app, host="0.0.0.0", port=8000)