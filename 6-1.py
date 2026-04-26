from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models import User

app = FastAPI()
security = HTTPBasic()


USER_DATA = [
    User(**{"username": "user1", "password": "pass1"}),
    User(**{"username": "user2", "password": "pass2"})
]

def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user

@app.get("/login")
def login(user: User = Depends(authenticate_user)):
    return {"message": "You got my secret, welcome"}