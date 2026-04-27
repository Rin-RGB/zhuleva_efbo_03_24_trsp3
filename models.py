from pydantic import BaseModel
from typing import List

class UserBase(BaseModel):
    username: str
class UserRole(UserBase):
    roles: List[str]
class User(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"