from sqlalchemy.orm import Session

from app.db.repositories.property_type_repository import fetch_property_types


def retrieve_property_types(db: Session):
    return fetch_property_types(db)

