from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..database.session import get_db
from ..models.item import Item
from ..schemas.items import ItemUpdate, ItemCreate


def all(db: Session, skip: int = 0, limit: int = 100):
    items = db.query(Item).offset(skip).limit(limit).all()
    return items


def id(db: Session, item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return item


def name(db: Session, item_name: str):
    item = db.query(Item).filter(Item.name == item_name.lower()).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return item


def type(db: Session, item_type: str, skip: int = 0, limit: int = 100):
    items = db.query(Item).filter(
        Item.type == item_type.lower()).offset(skip).limit(limit).all()
    return items


def price(db: Session, min_price: float, max_price: float):
    items = db.query(Item).filter(
        Item.price.between(min_price, max_price)).all()
    return items


def aviable(db: Session, is_aviable: bool, skip: int = 0, limit: int = 100):
    items = db.query(Item).filter(Item.is_aviable ==
                                  is_aviable).offset(skip).limit(limit).all()
    return items


def create(db: Session, new_item: ItemCreate):
    item_existing = db.query(Item).filter(Item.name == new_item.name).first()
    if item_existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item registered, try updates"
        )

    item = Item(
        name=new_item.name.lower(),
        type=new_item.type.lower(),
        description=new_item.description,
        price=new_item.price
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def update(db: Session, item_id: int, update_data: ItemUpdate):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

    if update_data.name:
        name_registered = db.query(Item).filter(
            Item.name == update_data.name).first()
        if name_registered and name_registered.id != item_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item already registered"
            )

    update_item = update_data.model_dump(exclude_unset=True)
    for field, value in update_item.items():
        if hasattr(item, field):
            setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


def delete(db: Session, item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    db.delete(item)
    db.commit()
    return {"Message": "Item deleted successfully"}
