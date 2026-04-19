from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from ..database.session import get_db
from ..schemas.items import ItemCreate, ItemUpdate, ItemResponse
from ..services import items
from ..core.auth import verify_api_key


router = APIRouter(prefix="/worker")


# endpoint for create a new item, if not exists
@router.post("/new_item", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_a_new_item(item: ItemCreate, db: Session = Depends(get_db), key: str = Depends(verify_api_key)):
    return items.create(db, item)


# endpoint for update an item, if exists
@router.put("/update_item", response_model=ItemResponse)
def update_an_item(item_name: str, update_item: ItemUpdate, db: Session = Depends(get_db), key: str = Depends(verify_api_key)):
    return items.update(db, item_name, update_item)


@router.delete("/delete_item")
def delete_an_item(item_name: str, db: Session = Depends(get_db), key: str = Depends(verify_api_key)):
    return items.delete(db, item_name)
