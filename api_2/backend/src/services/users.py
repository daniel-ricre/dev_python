from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..schemas.users import UserCreate, UserUpdate
from ..models.user import User


def all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


def username(db: Session, user_name: str):
    user = db.query(User).filter(User.username ==
                                 user_name.capitalize()).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


def email(db: Session, user_email: str):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


def active(db: Session, user_active: bool, skip: int = 0, limit: int = 100):
    users = db.query(User).filter(User.is_active == user_active).offset(skip).limit(
        limit).all()

    return users


def create(db: Session, user: UserCreate):
    username_existing = db.query(User).filter(
        User.username == user.username).first()
    if username_existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    email_existing = db.query(User).filter(User.email == user.email).first()
    if email_existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = User(
        username=user.username.capitalize(),
        email=user.email,
        password=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update(db: Session, user_id: int, user_data: UserUpdate):
    user_existing = db.query(User).filter(User.id == user_id).first()
    if not user_existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user_data.username:
        username_existing = db.query(User).filter(
            User.username == user_data.username).first()
        if username_existing and username_existing.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

    if user_data.email:
        email_existing = db.query(User).filter(
            User.email == user_data.email).first()
        if email_existing and email_existing.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    update_data = user_data.model_dump(exclude_unset=True)

    for field, key in update_data.items():
        if hasattr(user_existing, field):
            setattr(user_existing, field, key)

    db.commit()
    db.refresh(user_existing)
    return user_existing


def delete(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()
    return {"Message": "User deleted successfully"}
