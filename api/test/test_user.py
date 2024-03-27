from fastapi.testclient import TestClient
from fastapi import Body,HTTPException,status,Depends
from ..auth.service import get_current_user,SECRET_KEY,ALGORITHM,oauth2_scheme,get_user,create_access_token
from jose import JWTError, jwt
from ..validation.validation import Token,TokenData
from ..index import app
from ..database.database import get_db,drop_tables
from sqlmodel import create_engine,SQLModel,Session
from ..model.model import User
import os
from dotenv import load_dotenv,find_dotenv
from datetime import timedelta
load_dotenv(find_dotenv())
conn_str = os.environ["TEST_DATABASE_KEY"]

engine = create_engine(conn_str)

SQLModel.metadata.create_all(engine)

def get_db_override():
    with Session(engine) as session:
        return session
    

def get_current_user_override(token:str = Depends(oauth2_scheme),db:Session = Depends(get_db_override)):
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

def test_read_main():
    client = TestClient(app=app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"hello world"}
    

def test_create_user():
        
    app.dependency_overrides[get_db] = get_db_override
    
    client = TestClient(app=app)
    response = client.post("api/signup",json={"user_name":"adminn","email":"adminn@gmail.com","hashed_password":"password"})
    print(response)
    data = response.json()
    assert response.status_code == 200
    app.dependency_overrides = {}

def test_login_user():

    app.dependency_overrides[get_db] = get_db_override

    client = TestClient(app=app)
    response = client.post("api/login",data={"username":"adminn","password":"password"})
    assert response.status_code == 200
    app.dependency_overrides = {}


def test_get_todo():
    app.dependency_overrides[get_db] = get_db_override
    app.dependency_overrides[get_current_user] = get_current_user_override
    mock_user = {"user_name":"adminn","email":"adminn@gmail.com","hashed_password":"password"}
    mock_token = create_access_token({"sub":mock_user["user_name"]},timedelta(minutes=60))
    client = TestClient(app=app)
    response = client.get("api/todos",headers={"Authorization":f"bearer {mock_token}"})
    assert response.status_code == 200
    app.dependency_overrides = {}
  
def test_create_todo():
    app.dependency_overrides[get_db] = get_db_override
    app.dependency_overrides[get_current_user] = get_current_user_override
    mock_user = {"user_name":"adminn","email":"adminn@gmail.com","hashed_password":"password"}
    mock_token = create_access_token({"sub":mock_user["user_name"]},timedelta(minutes=60))
    client = TestClient(app=app)
    response = client.post("api/createtodo",json={"title":"todo title","description":"this is the description of the todo"},headers={"Authorization":f"bearer {mock_token}"})
    assert response.status_code == 200
    app.dependency_overrides = {}

def test_update_todo():
    app.dependency_overrides[get_db] = get_db_override
    app.dependency_overrides[get_current_user] = get_current_user_override
    mock_user = {"user_name":"adminn","email":"adminn@gmail.com","hashed_password":"password"}
    mock_token = create_access_token({"sub":mock_user["user_name"]},timedelta(minutes=60))
    client = TestClient(app=app)
    response = client.put("api/updatetodo",params={"todo_id":1},json={"title":"update title","description":"updated description"},headers={"Authorization":f"bearer {mock_token}"})
    assert response.status_code == 200
    app.dependency_overrides = {}

def test_delete_todo():
    app.dependency_overrides[get_db] = get_db_override
    app.dependency_overrides[get_current_user] = get_current_user_override
    mock_user = {"user_name":"adminn","email":"adminn@gmail.com","hashed_password":"password"}
    mock_token = create_access_token({"sub":mock_user["user_name"]},timedelta(minutes=60))
    client = TestClient(app=app)
    response = client.delete("api/deletetodo",params={"todo_id":1},headers={"Authorization":f"bearer {mock_token}"})
    assert response.status_code == 200
    app.dependency_overrides = {}


def test_drop_tables():
    db_dropped = drop_tables()
    assert db_dropped == "Tables dropped.."