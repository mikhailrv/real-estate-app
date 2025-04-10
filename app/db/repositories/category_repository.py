# app/db/repositories/category_repository.py
from sqlalchemy.orm import Session
from app.db.models import Category

def get_all_categories(db: Session):
    return db.query(Category).all()
