from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database.session import get_db
from ..schemas.items import ItemCreate, ItemUpdate, ItemResponse
from ..services import items


router = APIRouter(prefix="/items")


@router.post("/create", response_model=ItemResponse)
def create_item(new_item: ItemCreate, db: Session = Depends(get_db)):
    return items.create(db, new_item)


@router.get("/all", response_model=List[ItemResponse])
def get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return items.all(db, skip, limit)


@router.get("/by_name/{name}", response_model=ItemResponse)
def get_by_name(name: str, db: Session = Depends(get_db)):
    return items.name(db, name)


@router.get("/by_type/{type}", response_model=List[ItemResponse])
def get_by_type(item_type: str, db: Session = Depends(get_db)):
    return items.type(db, item_type)


@router.get("/by_price/{price}", response_model=List[ItemResponse])
def get_by_price(min_price: float, max_price: float, db: Session = Depends(get_db)):
    return items.price(db, min_price, max_price)


@router.get("/by_aviable/{aviable}", response_model=List[ItemResponse])
def get_by_aviable(is_aviable: bool, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return items.aviable(db, is_aviable, skip, limit)


@router.put("/update/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, update_data: ItemUpdate, db: Session = Depends(get_db)):
    return items.update(db, item_id, update_data)


@router.delete("/delete/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    return items.delete(db, item_id)
