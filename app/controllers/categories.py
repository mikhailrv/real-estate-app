from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.category_service import get_categories
from app.db.database import get_db

router = APIRouter(
    tags=["Categories"]
)
@router.get("/categories/")
def read_categories(db: Session = Depends(get_db)):
    return get_categories(db)


