from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database.session import get_db
from ..schemas.users import UserCreate, UserUpdate, UserResponse
from ..services.users import get_all, update, delete


router = APIRouter(prefix="/admin")


@router.get("/all", response_model=List[UserResponse])
def all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all(db, skip, limit)


@router.put("/update", response_model=UserResponse)
def update_user(user_update: UserUpdate, user_id: int, db: Session = Depends(get_db)):
    return update(db, user_id, user_update)


@router.delete("/delete")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return delete(db, user_id)
