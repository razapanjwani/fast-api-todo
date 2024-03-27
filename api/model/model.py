from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UUID
from pydantic import BaseModel
import uuid 
from typing import Optional
from sqlmodel import Field,SQLModel

# class User(Base):
#     __tablename__ = "users"
#     id = Column(UUID ,primary_key=True,default=uuid.uuid4)
#     email:str = Column(String,nullable=False,unique=True)
#     hashed_password:str = Column(String,nullable=False)
#     user_name:str = Column(String,nullable=False) 


# class Todo(Base):
#     __tablename__ = "todos"
#     id:UUID = Column(UUID, primary_key=True, index=True,default=uuid.uuid4)
#     title:str = Column(String, index=True)
#     description:str = Column(String, index=True)
#     user_id:int = Column(UUID,ForeignKey("users.id",ondelete="CASCADE"))

class User(SQLModel,table = True):
    id:Optional[int] = Field(default=None,primary_key=True)
    email:str = Field(nullable=False,unique=True)
    hashed_password:str = Field(nullable=False)
    user_name:str = Field(nullable=False)  
    

class Todo(SQLModel,table =True):
    id:Optional[int] = Field(default=None,primary_key=True)
    title:str = Field(index=True)
    description:str = Field(index=True)
    user_id:Optional[int] = Field(foreign_key="user.id",default=None)  
    
