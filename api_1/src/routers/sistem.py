from fastapi import APIRouter

router = APIRouter()


@router.head("/")
def get_health():
    return


@router.get("/")
def get_root():
    return {"status": "running"}
