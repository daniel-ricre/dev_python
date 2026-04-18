from ..services.user_crud import create_user, update
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status, Security
from ..database.session import get_db
from ..schemas.user_schemas import UserResponse, UserCreate, UserResponseAdmin, UserUpdate
from .router_admin import verify_api_key

router = APIRouter(prefix="/public")


@router.post("/create_user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(new_user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, new_user)


@router.put("/update_user", response_model=UserResponseAdmin)
def update_user(new_data: UserUpdate, user_id: int, db: Session = Depends(get_db), api_key: str = Security(verify_api_key)):
    return update(db, user_id, new_data)
