from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models.date import DateT
from ..schemas.dates import DateResponse, DateCreate, DateUpdate


def create(db: Session, date: DateCreate):
    new_date = DateT(
        year=date.year,
        mont=date.mont,
        day=date.day,
        aviable=date.aviable,
        unaviable=date.unaviable
    )

    db.add(new_date)
    db.commit()
    db.refresh(new_date)
    return new_date


def update(db: Session, date_id: int, update_date: DateUpdate):
    date = db.query(DateT).filter(DateT.id == date_id).first()
    if not date:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fecha no encontrada"
        )

    new_data = update_date.model_dump(exclude_unset=True)
    for field, value in new_data.items():
        if hasattr(date, field):
            setattr(date, field, value)

    db.commit()
    db.refresh(date)
    return date


def mont(db: Session, date_mont: str):
    return db.query(DateT).filter(DateT.mont == date_mont).all()


def year(db: Session, date_year: str):
    return db.query(DateT).filter(DateT.year == date_year).all()


def year_mont_day(db: Session, year: str, mont: str, day: str):
    date = db.query(DateT).filter(
        DateT.year == year and DateT.mont == mont and DateT.day == day).first()
    if not date:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fecha no encontrada"
        )


def delete(db: Session, date_id: int):
    date = db.query(DateT).filter(DateT.id == date_id).first()
    if not date:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fecha no enontrada"
        )
