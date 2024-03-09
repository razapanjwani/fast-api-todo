from pydantic import BaseModel,EmailStr

from uuid import UUID
from datetime import timedelta

class TodoCreate(BaseModel):
    title:str
    description:str
    
class TodoUpdate(BaseModel):    
    title:str
    description:str

class TodoResponse(BaseModel):
    id:UUID
    title:str
    description:str
    user_id:UUID

class UserCreate(BaseModel):
    user_name:str
    email:EmailStr
    hashed_password:str

class UserResponse(BaseModel):
    id:UUID | int
    email:EmailStr
    

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int | timedelta
    refresh_token: str

class TokenData(BaseModel):
    username: str | None = None
    id: UUID | None = None

class UserLogin(BaseModel):
    email:EmailStr
    hashed_password:str