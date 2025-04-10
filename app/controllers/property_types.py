from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.listings import PropertyTypeResponse
from typing import List
from app.services.property_type_service import retrieve_property_types

router = APIRouter()

@router.get("/property_types", response_model=List[PropertyTypeResponse])
def get_property_types(db: Session = Depends(get_db)):
    return retrieve_property_types(db)