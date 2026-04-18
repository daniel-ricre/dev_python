from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from ..schemas.auth import LoginRequest
from ..models.user import User
from ..config import TOKEN_ACCESS_EXPIRE_MINUTES
from ..utils.auth import create_access_token


def autenticate_user(db: Session, username_or_email: str, password: str):
    pass
