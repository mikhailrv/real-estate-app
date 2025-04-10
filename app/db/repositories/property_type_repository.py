from sqlalchemy.orm import Session
from app.db.models import PropertyType


def fetch_property_types(db: Session):
    return db.query(PropertyType).all()