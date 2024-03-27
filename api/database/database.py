from sqlalchemy.orm import DeclarativeBase,sessionmaker
from sqlmodel import create_engine,Session,SQLModel
from dotenv import load_dotenv,find_dotenv
import os
load_dotenv(find_dotenv())

engine = create_engine(os.environ["DATABASE_KEY"])
test_engine = create_engine(os.environ["TEST_DATABASE_KEY"])

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    with Session(engine) as session:
        yield session
    

def drop_tables():
    print("Dropping tables..")
    SQLModel.metadata.drop_all(test_engine)
    return ("Tables dropped..")
        
        

