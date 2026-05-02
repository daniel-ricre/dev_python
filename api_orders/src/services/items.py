from sqlalchemy.orm import Session
from ..schemas.items import ItemCreate, ItemUpdate
from ..models.item import Item
from fastapi import HTTPException, status


def create(db: Session, item: ItemCreate):
    """Create an item, if not exists"""
    item_exsiting = db.query(Item).filter(
        Item.name == item.name).first()
    if item_exsiting:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Name Item already registered, try update {item_exsiting}"
        )

    new_item = Item(
        name=item.name,
        price=item.price,
        stock=item.stock
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def update(db: Session, item_name: str, update_item: ItemUpdate):
    """Update an item, if exists"""
    item = db.query(Item).filter(Item.name == item_name).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no found"
        )

    if update_item.name:
        item_existing = db.query(Item).filter(
            Item.name == update_item.name).first()
        if item_existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item already registered"
            )

    update_data = update_item.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(item, field):
            setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


def delete(db: Session, item_name: str):
    """delete an item, if exists"""
    item = db.query(Item).filter(Item.name == item_name).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

    db.delete(item)
    db.commit()
    return {"Item deleted successfully"}


def all(db: Session, skip: int = 0, limit: int = 10):
    """Get all items"""
    return db.query(Item).offset(skip).limit(limit).all()


def name(db: Session, item_name: str):
    """Get name item, if exists"""
    item = db.query(Item).filter(Item.name == item_name).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return item
