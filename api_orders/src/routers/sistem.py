from fastapi import APIRouter

router = APIRouter(prefix="/sistem")


@router.head("/")
def get_health():
    return
