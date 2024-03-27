from datetime import timedelta, datetime
from typing import Annotated
from fastapi import Depends,HTTPException
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from ..database.database import get_db
from ..database.database import SessionLocal
from ..model.model import User
from sqlmodel import Session,select
from ..validation.validation import UserCreate
from ..utils.helper import get_password_hash
from dotenv import load_dotenv ,find_dotenv
import os
load_dotenv(find_dotenv())

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
ouath2_bearer = OAuth2PasswordBearer(tokenUrl="token")


def db_signup_user(user_data:UserCreate,db:Session):
    existing_user = db.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User already exists")
    hashed_password = get_password_hash(user_data.hashed_password)
    user = User(email = user_data.email,hashed_password = hashed_password,user_name = user_data.user_name)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def  get_user(db:Session,user_name:str):
    if user_name is None:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,headers={"WWW-Authenticate": 'Bearer'},detail={"error": "invalid_token", "error_description": "The access token expired"})

    user = db.exec(select(User).where(User.user_name == user_name)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return user

def get_user_by_id(db:Session,user_id:int):
    if user_id is None:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,headers={"WWW-Authenticate": 'Bearer'},detail={"error": "invalid_token", "error_description": "The access token expired"})

    user = db.exec(select(User).where(User.id == user_id)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return user

def get_user_by_email(db:Session,email:str):
    if email is None:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,headers={"WWW-Authenticate": 'Bearer'},detail={"error": "invalid_token", "error_description": "The access token expired"})

    user = db.exec(select(User).where(User.email == email)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return user






