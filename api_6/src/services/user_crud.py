from ..schemas.user_schemas import UserCreate, UserUpdate
from ..models.user_models import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import bcrypt


def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt con truncamiento a 72 bytes"""
    # Truncar a 72 bytes si es necesario
    password_bytes = password.encode('utf-8')[:72]
    # Generar salt y hashear
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash"""
    plain_password_bytes = plain_password.encode('utf-8')[:72]
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)


def get_users(db: Session, skip: int = 0, limit: int = 50):
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, new_user: UserCreate):
    # Verificar si el email ya existe
    email_existing = db.query(User).filter(
        User.email == new_user.email).first()
    if email_existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Verificar si el username ya existe
    username_existing = db.query(User).filter(
        User.username == new_user.username).first()
    if username_existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Hashear la contraseña
    hashed_password = hash_password(new_user.password)

    # Crear el usuario
    user_data = new_user.model_dump()
    user_data["password"] = hashed_password
    user = User(**user_data)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update(db: Session, user_id: int, new_data: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if new_data.username:
        username_existing = db.query(User).filter(
            User.username == new_data.username).first()
        if username_existing and username_existing.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

    if new_data.email:
        email_existing = db.query(User).filter(
            User.email == new_data.email).first()
        if email_existing and email_existing.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    update_data = new_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(user, field):
            setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db.delete(user)
    db.commit()
    return {"Message": "User deleted successfully"}
