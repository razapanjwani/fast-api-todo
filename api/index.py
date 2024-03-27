from fastapi import FastAPI,Depends,HTTPException,Form,Body
from typing import Optional
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from .crud.crud import TodoCrud
from .database.database import get_db,engine
from starlette import status
from sqlalchemy.orm import Session
from .validation.validation import TodoCreate,TodoUpdate,TodoResponse,UserCreate,UserResponse,Token
from .auth.service import service_signup_users,authenticate_user,get_current_user,create_access_token,create_refresh_token,token_service
from .model.model import *
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel
from typing import Annotated    
app:FastAPI = FastAPI(docs_url="/docs",debug=True)

todocrud = TodoCrud()
SQLModel.metadata.create_all(bind=engine)


@app.get("/")
def main_hello():
    return {"message":"hello world"}

@app.get("/api/todos", response_model=list[TodoResponse])
def get_todos(db:Session = Depends(get_db),user = Depends(get_current_user)):
    return todocrud.crud_get_todo(db,user=user)

@app.post("/api/createtodo",response_model=TodoCreate)
def create_todo(todo_data:TodoCreate = Body() ,db:Session = Depends(get_db),user = Depends(get_current_user)):
    return todocrud.crud_create_todo(todo_data,db,user)
    

@app.put("/api/updatetodo")
def update_todo(todo_id,updated_todo:TodoUpdate = Body(),db:Session = Depends(get_db),user = Depends(get_current_user)):
    todocrud.crud_update_todo(todo_id,updated_todo,db)
    return {"message":"Todo updated"}

@app.delete("/api/deletetodo")
def delete_todo(todo_id,db:Session = Depends(get_db),user = Depends(get_current_user)):
    return todocrud.crud_delete_todo(todo_id,db)
    

@app.post("/api/signup",response_model=UserResponse)
def sign_up(user_data:UserCreate = Body(),db:Session = Depends(get_db)):
    try:
        return service_signup_users(user_data,db)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    

        
@app.post("/api/login",response_model=Token)
def login_user(form_data:OAuth2PasswordRequestForm = Depends() ,db:Session = Depends(get_db)):
    user = authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=7)
    refresh_token = create_refresh_token(data={"id": user.id}, expires_delta=refresh_token_expires)
    return Token(access_token=access_token, token_type="bearer", expires_in= access_token_expires, refresh_token=refresh_token)



@app.post("/api/token",response_model=Token)
def token_manager(
    refresh_token:Optional[str] = Form(),
    db:Session = Depends(get_db)
):
    return token_service(refresh_token,db)

