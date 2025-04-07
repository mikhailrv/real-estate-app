from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Category

router = APIRouter()

# работает
@router.get("/categories/")
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

