from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database.session import get_db
from ..schemas.items import ItemResponse
from ..services import items

router = APIRouter(prefix="/clients")


# endpoint for get root
@router.get("/")
def get_root():
    return {"Welcome to 'El Tornillo Feliz'"}


# endpoint for get all items
@router.get("/all_items", response_model=List[ItemResponse])
def get_all_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return items.all(db, skip, limit)


# endpoint for get item by name
@router.get("/name_item", response_model=ItemResponse)
def get_item_by_name(item_name: str, db: Session = Depends(get_db)):
    return items.name(db, item_name)
