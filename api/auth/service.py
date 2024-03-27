from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session,select
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from ..model.model import User
from ..auth.index import get_user,SECRET_KEY,ALGORITHM,get_user_by_id,ouath2_bearer,db_signup_user
from ..utils.helper import verify_password
from ..validation.validation import Token,TokenData
from uuid import UUID
from ..database.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def authenticate_user(db:Session,user_name:str,password:str):
    try:
        user = get_user(db,user_name)  
    except:
        return False

    if not verify_password(password,user.hashed_password):
        return False
    return user

def create_access_token(data:dict,expires_delta:timedelta | None):
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp":expires})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data:dict,expires_delta:timedelta | None):
    to_encode = data.copy()

    if 'id' in to_encode and isinstance(to_encode['id'], UUID):
        to_encode['id'] = str(to_encode['id'])

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)

    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def validate_refresh_token(db:Session,refresh_token:str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Refresh Token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id_str: str | None = (payload.get("id"))

        if user_id_str is None:
            raise credentials_exception
        user_id = UUID(user_id_str)

        token_data = TokenData(id = user_id)
        if token_data.id is None:
            raise credentials_exception
        user = get_user_by_id(db, token_data.id)
        if user is None:
            raise credentials_exception
        return user

    except JWTError:
        return credentials_exception

def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_name = payload.get("sub")
        if user_name is None:
            raise credentials_exception

        token_data = TokenData(username=user_name)
        
    except JWTError:
        raise credentials_exception
    if token_data.username is None:
        raise credentials_exception
    user = get_user(db, user_name=token_data.username)
    if user is None:
        raise credentials_exception
    return user   


def service_signup_users(user_data, db: Session):
    
    try:
        return db_signup_user(user_data, db)
    except Exception as e:
        # Re-raise the exception to be handled in the web layer
        raise e
    except Exception as e:
        # Re-raise general exceptions to be handled in the web layer
        raise e
    
def token_service(refresh_token:str,db:Session):
    user = validate_refresh_token(db,refresh_token)
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(data={"sub": user.user_name}, expires_delta=access_token_expires)

    refresh_token_expires = timedelta(days=7)
    rotated_refresh_token = create_refresh_token(data={"id": user.id}, expires_delta=refresh_token_expires)

    token = {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": access_token_expires,
        "refresh_token": rotated_refresh_token
    }

    return token

