from decimal import Decimal
from app.db.models import Listing, ListingPhoto
from app.db.repositories.listing_repository import (
    get_favorite,
    get_listings,
    get_listing_by_id,
    create_listing,
    add_photo_to_listing,
    delete_listing,
    add_to_favorites,
    remove_from_favorites,
    get_favorites
)
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.listings import ListingCreate

def get_ads(
    db: Session,
    categories: Optional[List[int]] = None,
    city: Optional[str] = None,
    price_min: Optional[Decimal] = None,
    price_max: Optional[Decimal] = None,
    area_min: Optional[Decimal] = None,
    area_max: Optional[Decimal] = None,
    rooms: Optional[List[int]] = None
):
    return get_listings(
        db, categories, city, price_min, price_max, area_min, area_max, rooms
    )


def get_ad_by_id(db: Session, ad_id: int):
    ad = get_listing_by_id(db, ad_id)
    ad.photos = db.query(ListingPhoto).filter(ListingPhoto.listing_id == ad_id).all()
    
    return ad


def create_ad(db: Session, user_id: int, listing_data: ListingCreate):
    listing_data_dict = listing_data.dict()

    new_listing = create_listing(db, user_id, listing_data_dict)
        
    return new_listing


def upload_photo_to_ad(db: Session, listing_id: int, file_path: str):
    return add_photo_to_listing(db, listing_id, file_path)


def delete_listing_data(db: Session, ad_id: int):
    delete_listing(db, ad_id)

def create_or_delete_favorite(db: Session, user_id: int, ad_id: int):
    existing_fav = get_favorite(db, user_id, ad_id)
    if existing_fav:
        remove_from_favorites(db, user_id, ad_id)
        return{"detail": "Удалено из избранного"}
    add_to_favorites(db, user_id, ad_id)
    return{"detail": "Добавлено в избранное"}

def get_user_favorites(db: Session, user_id: int):
    return get_favorites(db, user_id)

def update_listing_data(listing: Listing, update_data: dict) -> Listing:
    for field, value in update_data.items():
        setattr(listing, field, value)
    return listing