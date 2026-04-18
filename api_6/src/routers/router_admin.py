from ..services.user_crud import get_users, get_user_by_id, delete_user
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status, HTTPException, Security
from fastapi.security import APIKeyHeader
from ..database.session import get_db
from typing import List
from ..schemas.user_schemas import UserResponseAdmin
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

router = APIRouter(prefix="/admin")

# Configurar autenticación por Header
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


@router.get("/users", response_model=List[UserResponseAdmin])
def get_all_users(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    api_key: str = Security(verify_api_key)  # Autenticación automática
):
    return get_users(db, skip, limit)


@router.get("/user/{user_id}", response_model=UserResponseAdmin)
def get_user_id(
    user_id: int,
    db: Session = Depends(get_db),
    api_key: str = Security(verify_api_key)  # Autenticación automática
):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.delete("/user/{user_id}")
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    api_key: str = Security(verify_api_key)  # Autenticación automática
):
    return delete_user(db, user_id)
