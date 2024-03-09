from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UUID
from sqlalchemy.orm import relationship,Mapped
from ..database.database import Base
from pydantic import BaseModel
import uuid 
from typing import Optional

class User(Base):
    __tablename__ = "users"
    id = Column(UUID ,primary_key=True,default=uuid.uuid4)
    email:str = Column(String,nullable=False,unique=True)
    hashed_password:str = Column(String,nullable=False)
    user_name:str = Column(String,nullable=False) 


class Todo(Base):
    __tablename__ = "todos"
    id:UUID = Column(UUID, primary_key=True, index=True,default=uuid.uuid4)
    title:str = Column(String, index=True)
    description:str = Column(String, index=True)
    user_id:int = Column(UUID,ForeignKey("users.id",ondelete="CASCADE"))
