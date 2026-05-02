from fastapi import APIRouter, Depends, status, Form
from sqlalchemy.orm import Session
from ..database.session import get_db
from ..schemas.users import UserCreate, UserUpdate, UserResponse
from ..services.users import create

router = APIRouter(prefix="/users")


@router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create(db, user)
