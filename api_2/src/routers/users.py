from fastapi import APIRouter, Depends, Security, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from typing import List
from ..database.session import get_db
from ..schemas.users import UserCreate, UserResponse, UserUpdate
from ..services import users
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SECRET_KEY")


router = APIRouter(prefix="/users")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)


def verify_api_key(api_key: str = Security(api_key_header)):
    """Verifica que la API key sea válida"""
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "APIKey"},
        )
    return api_key


@router.post("/create", response_model=UserResponse)
def create_new_user(new_user: UserCreate, db: Session = Depends(get_db)):
    return users.create(db, new_user)


@router.get("/all", response_model=List[UserResponse])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), api_key: str = Security(verify_api_key)):
    return users.all(db, skip, limit)


@router.get("/by_id/{id}", response_model=UserResponse)
def get_by_id(user_id: int, db: Session = Depends(get_db), api_key: str = Security(verify_api_key)):
    return users.id(db, user_id)


@router.get("/by_username/{username}", response_model=UserResponse)
def get_by_username(username: str, db: Session = Depends(get_db), api_key: str = Security(verify_api_key)):
    return users.username(db, username)


@router.get("/by_email/{email}", response_model=UserResponse)
def get_by_email(user_email: str, db: Session = Depends(get_db), api_key: str = Security(verify_api_key)):
    return users.email(db, user_email)


@router.get("/by_actives/{active}", response_model=List[UserResponse])
def get_by_actives(active: bool, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), api_key: str = Security(verify_api_key)):
    return users.active(db, active, skip, limit)


@router.put("/update/{id}", response_model=UserResponse)
def update_user(user_id: int, update_data: UserUpdate, db: Session = Depends(get_db), api_key: str = Security(verify_api_key)):
    return users.update(db, user_id, update_data)


@router.delete("/delete/{id}")
def delete_user(user_id: int, db: Session = Depends(get_db), api_key: str = Security(verify_api_key)):
    return users.delete(db, user_id)
