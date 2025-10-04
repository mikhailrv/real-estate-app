from decimal import Decimal
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from app.db.repositories.listing_repository import get_listing_by_id, update_listing
from app.services.listing_service import (
    create_or_delete_favorite,
    delete_listing_data,
    get_ads,
    get_ad_by_id,
    create_ad,
    has_favorite,
    update_listing_data,
    upload_photo_to_ad,
    get_user_favorites
)
from app.db.database import get_db
from app.schemas.listings import ListingResponse, PhotoResponse, ListingCreate
from app.services.auth_service import get_current_user

router = APIRouter(
    tags=["Listings"]
)

@router.get("/ads/", response_model=List[ListingResponse])
def get_ads_route(
    db: Session = Depends(get_db),
    categories: Optional[List[int]] = Query(None),
    city: Optional[str] = Query(None),
    price_min: Optional[Decimal] = Query(None),
    price_max: Optional[Decimal] = Query(None),
    area_min: Optional[Decimal] = Query(None),
    area_max: Optional[Decimal] = Query(None),
    rooms: Optional[List[int]] = Query(None),
):
    return get_ads(
        db, categories, city, price_min, price_max, area_min, area_max, rooms
    )


@router.post("/ads/{listing_id}/upload-photo/", response_model=PhotoResponse)
def upload_photo(
    listing_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    allowed_extensions = {"jpg", "jpeg", "png"}
    extension = file.filename.split(".")[-1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Файл должен быть JPG или PNG")

    file_path = f"static/uploads/{listing_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    photo = upload_photo_to_ad(db, listing_id, file_path)

    return {"photo_id": photo.photo_id, "photo_url": photo.photo_url}

@router.get("/ads/{ad_id}/", response_model=ListingResponse)
def get_ad_route(ad_id: int, db: Session = Depends(get_db)):
    ad = get_ad_by_id(db, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    return ad

@router.post("/ads/", response_model=ListingResponse)
def create_ad_route(
    listing_data: ListingCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_ad(db, current_user.user_id, listing_data)

@router.put("/ads/{ad_id}/", response_model=ListingResponse)
def update_ad(
    ad_id: int,
    ad_data: ListingCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    ad = get_listing_by_id(db, ad_id)

    if not ad:
        raise HTTPException(status_code=404, detail="Объявление не найдено")

    if ad.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Нет доступа")

    updated_ad = update_listing_data(ad, ad_data.model_dump(exclude_unset=True))
    
    return update_listing(db, updated_ad)

@router.delete("/ads/{ad_id}/")
def delete_ad(
    ad_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    ad = get_listing_by_id(db, ad_id)

    if not ad:
        raise HTTPException(status_code=404, detail="Объявление не найдено")

    if ad.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Нет доступа")

    delete_listing_data(db, ad.listing_id)

    return {"msg": "Объявление удалено"}

@router.post("/favorites/{ad_id}/", status_code=201)
def add_to_favorites(
    ad_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    message = create_or_delete_favorite(db, user.user_id, ad_id)
    return {"message": message}

@router.get("/favorites/", response_model=List[ListingResponse])
def get_favorites(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return get_user_favorites(db, user.user_id)

@router.get("/favorites/{ad_id}")
def check_favorite(ad_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    favorite = has_favorite(db, current_user.user_id, ad_id)
    return {"is_favorite": bool(favorite)}