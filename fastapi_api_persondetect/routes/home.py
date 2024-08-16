from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def home():
    return 'Home - Detector de carros API Flask'
