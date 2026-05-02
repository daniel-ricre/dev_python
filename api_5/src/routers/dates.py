from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, Security
from typing import List
from ..database.session import get_db
from ..schemas.dates import DateCreate, DateUpdate, DateResponse
from ..models.date import DateT
from ..services import dates
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("SECRET_KEY")

router = APIRouter(prefix="/fecha")


@router.post("/crear", response_model=DateResponse, status_code=status.HTTP_201_CREATED)
def crear(fecha: DateCreate, db: Session = Depends(get_db)):
    return dates.create(db, fecha)


@router.get("/completa", response_model=DateResponse)
def buscar_fecha_especifica(año: str, mes: str, dia: str, db: Session = Depends(get_db)):
    return dates.year_mont_day(db, año, mes, dia)
