from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def get_root():
    return {"estado": "Corriendo",
            "base_datos": "Conectada"}


@router.head("/")
def get_helath():
    return
