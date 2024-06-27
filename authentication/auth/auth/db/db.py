from typing import Annotated
from dotenv import load_dotenv , find_dotenv
import os
from fastapi import Depends
from sqlmodel import create_engine , SQLModel ,Session




_: bool = load_dotenv(find_dotenv()) 

key = os.environ.get('URL_DB')

if key is None:
    raise ValueError('Database key not found')


engine = create_engine(key )

def create_db_and_tables():
    print("Creating Tables...")
    SQLModel.metadata.create_all(engine  )

def get_db():
    with Session(engine) as session:
        yield session

