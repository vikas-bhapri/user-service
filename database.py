from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_CONNECTION_STRING")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a Session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class
Base = declarative_base()

# Create a function to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()