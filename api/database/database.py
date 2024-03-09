from sqlalchemy.orm import DeclarativeBase,sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv,find_dotenv
import os
load_dotenv(find_dotenv())

engine = create_engine(os.environ["DATABASE_KEY"])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
class Base(DeclarativeBase):
    pass

