from app.db.repositories.category_repository import get_all_categories
from sqlalchemy.orm import Session

def get_categories(db: Session):
    return get_all_categories(db)
