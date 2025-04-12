from sqlalchemy.orm import Session
from app.db.models import Listing, ListingPhoto, SavedListing, Category
from typing import List, Optional
from decimal import Decimal

from app.schemas.listings import PhotoResponse

def get_listings(
    db: Session,
    categories: Optional[List[int]] = None,
    city: Optional[str] = None,
    price_min: Optional[Decimal] = None,
    price_max: Optional[Decimal] = None,
    area_min: Optional[Decimal] = None,
    area_max: Optional[Decimal] = None,
    rooms: Optional[List[int]] = None
):
    query = db.query(Listing)

    filters = []
    if price_min is not None:
        filters.append(Listing.price >= price_min)
    if price_max is not None:
        filters.append(Listing.price <= price_max)
    if area_min is not None:
        filters.append(Listing.area >= area_min)
    if area_max is not None:
        filters.append(Listing.area <= area_max)

    query = query.filter(*filters)

    if city:
        query = query.filter(Listing.city == city)

    if categories:
        query = query.join(Listing.categories).filter(Category.category_id.in_(categories))

    if rooms:
        query = query.filter(Listing.rooms.in_(rooms))

    listings = query.all()

    for listing in listings:
        listing.images = [PhotoResponse(photo_id=photo.photo_id, photo_url=photo.photo_url) for photo in listing.photos]

    return listings


def get_listing_by_id(db: Session, ad_id: int):
    listing = db.query(Listing).filter(Listing.listing_id == ad_id).first()
    listing.images = [PhotoResponse(photo_id=photo.photo_id, photo_url=photo.photo_url) for photo in listing.photos]
    return listing


def create_listing(db: Session, user_id: int, listing_data: dict):
    category_ids = listing_data.pop("category_ids", [])


    new_listing = Listing(**listing_data, user_id=user_id)
    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)

    if category_ids:
        categories = db.query(Category).filter(Category.category_id.in_(category_ids)).all()
        if categories:
            new_listing.categories = categories
            db.commit()
            db.refresh(new_listing)

    return new_listing


def add_photo_to_listing(db: Session, listing_id: int, file_path: str):
    photo = ListingPhoto(listing_id=listing_id, photo_url=file_path)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


def delete_listing(db: Session, ad_id: int):
    ad = db.query(Listing).filter(Listing.listing_id == ad_id).first()
    db.delete(ad)
    db.commit()


def add_to_favorites(db: Session, user_id: int, ad_id: int):
    favorite = SavedListing(user_id=user_id, listing_id=ad_id)
    db.add(favorite)
    db.commit()
    return favorite


def remove_from_favorites(db: Session, user_id: int, ad_id: int):
    existing_fav = db.query(SavedListing).filter_by(user_id=user_id, listing_id=ad_id).first()
    db.delete(existing_fav)
    db.commit()
    return 


def get_favorites(db: Session, user_id: int):
    favs = db.query(Listing).join(SavedListing).filter(SavedListing.user_id == user_id).all()
    for fav in favs:
        fav.images = [PhotoResponse(photo_id=photo.photo_id, photo_url=photo.photo_url) for photo in fav.photos]
    return favs

def update_listing(db: Session, listing: Listing) -> Listing:
    db.commit()
    db.refresh(listing)
    return listing

def get_favorite(db: Session, user_id: int, ad_id: int):
    favorite = db.query(SavedListing).filter_by(user_id = user_id, listing_id = ad_id).first()
    return favorite