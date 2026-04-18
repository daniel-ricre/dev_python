from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

try:
    DATABASE_URL = os.getenv("DATABASE_URL_ONLINE")
    engine = create_engine(DATABASE_URL)

except:
    dir_database = os.getenv("DATABASE_URL_LOCAL")
    DATABASE_URL = f"sqlite:///api_5/{dir_database}"
    engine = create_engine(DATABASE_URL, connect_args={
                           "check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
