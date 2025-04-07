from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import PropertyType
from app.schemas.listings import PropertyTypeResponse
from typing import List

router = APIRouter()

# работает
@router.get("/property_types", response_model=List[PropertyTypeResponse])
def get_property_types(db: Session = Depends(get_db)):
    return db.query(PropertyType).all()