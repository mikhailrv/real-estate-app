from decimal import Decimal
import os
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from typing import Optional, List
from app.schemas.listings import ListingResponse, PhotoResponse, ListingCreate
from app.db.models import Listing, Category, ListingPhoto, User, SavedListing
from app.api.auth import get_current_user

router = APIRouter()

# Работает
@router.get("/ads/", response_model=List[ListingResponse])
def get_ads(
    db: Session = Depends(get_db),
    categories: Optional[List[int]] = Query(None),
    city: Optional[str] = Query(None),
    price_min: Optional[Decimal] = Query(None),
    price_max: Optional[Decimal] = Query(None),
    area_min: Optional[Decimal] = Query(None),
    area_max: Optional[Decimal] = Query(None),
    rooms: Optional[List[int]] = Query(None),
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
        listing.images = [photo.photo_url for photo in listing.photos]

    return listings


UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Работает
@router.post("/ads/{listing_id}/upload-photo/", response_model=PhotoResponse)
def upload_photo(listing_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    allowed_extensions = {"jpg", "jpeg", "png"}
    extension = file.filename.split(".")[-1].lower()
    if extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Файл должен быть JPG или PNG")

    file_path = os.path.join(UPLOAD_FOLDER, f"{listing_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
     
    photo = ListingPhoto(listing_id=listing_id, photo_url=file_path)
    db.add(photo)
    db.commit()
    db.refresh(photo)

    return {"photo_id": photo.photo_id, "photo_url": photo.photo_url}

# Работает
@router.get("/ads/{ad_id}/", response_model=ListingResponse)
def get_ad(ad_id: int, db: Session = Depends(get_db)):
    ad = db.query(Listing).filter(Listing.listing_id == ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Объявление не найдено")

    ad.photos = db.query(ListingPhoto).filter(ListingPhoto.listing_id == ad_id).all()

    return ad

# работает
@router.post("/ads/", response_model=ListingResponse)
def create_ad(
    listing_data: ListingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    new_listing = Listing(
        description=listing_data.description,
        price=listing_data.price,
        property_type_id=listing_data.property_type_id,
        city=listing_data.city,
        street=listing_data.street,
        house_number=listing_data.house_number,
        apartment_number=listing_data.apartment_number,
        area=listing_data.area,
        rooms=listing_data.rooms,
        bathrooms=listing_data.bathrooms,
        latitude=listing_data.latitude,
        longitude=listing_data.longitude,
        user_id=current_user.user_id,
    )

    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)

    if listing_data.category_ids:
        categories = db.query(Category).filter(Category.category_id.in_(listing_data.category_ids)).all()
        if categories:
            new_listing.categories = categories

    db.commit()
    db.refresh(new_listing)

    return new_listing

# работает
@router.put("/ads/{ad_id}/", response_model=ListingResponse)
def update_ad(
    ad_id: int,
    ad_data: ListingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    ad = db.query(Listing).filter(Listing.listing_id == ad_id).first()

    if not ad:
        raise HTTPException(status_code=404, detail="Объявление не найдено")

    if ad.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Нет доступа")

    for field, value in ad_data.model_dump(exclude_unset=True).items():
        setattr(ad, field, value)

    db.commit()
    db.refresh(ad)
    return ad


# работает
@router.delete("/ads/{ad_id}/")
def delete_ad(
    ad_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    ad = db.query(Listing).filter(Listing.listing_id == ad_id).first()

    if not ad:
        raise HTTPException(status_code=404, detail="Объявление не найдено")

    if ad.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Нет доступа")

    db.delete(ad)
    db.commit()
    return {"msg": "Объявление удалено"}

# работает
@router.post("/favorites/{ad_id}/", status_code=201)
def add_to_favorites(ad_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    existing_fav = db.query(SavedListing).filter_by(user_id=user.user_id, listing_id=ad_id).first()
    if existing_fav:
        db.delete(existing_fav)
        db.commit()
        return {"message": "Объявление удалено из избранного"}

    favorite = SavedListing(user_id=user.user_id, listing_id=ad_id)
    db.add(favorite)
    db.commit()
    return {"message": "Добавлено в избранное"}

# работает
@router.get("/favorites/", response_model=List[ListingResponse])
def get_favorites(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    favorites = db.query(Listing).join(SavedListing).filter(SavedListing.user_id == user.user_id).all()

    return favorites
    