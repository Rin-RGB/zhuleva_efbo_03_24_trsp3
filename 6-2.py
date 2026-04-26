from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models import User, UserInDB
import secrets
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto",  bcrypt__rounds=10)

app = FastAPI()
security = HTTPBasic()


fake_users_db: dict[str, UserInDB] = {}


def auth_user(credentials: HTTPBasicCredentials = Depends(security)) -> UserInDB:
    found_user = None
    for username, user in fake_users_db.items():
        if secrets.compare_digest(username, credentials.username):
            found_user = user
            break
    if found_user == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    if not pwd_context.verify(credentials.password, found_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return found_user


@app.post("/register")
async def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

    hashed = pwd_context.hash(user.password)
    user_in_db = UserInDB(username=user.username, hashed_password=hashed)
    fake_users_db[user.username] = user_in_db

    return {"message": "User registered successfully"}


@app.get("/login")
async def login(current_user: UserInDB = Depends(auth_user)):
    return {"message": f"Welcome, {current_user.username}"}