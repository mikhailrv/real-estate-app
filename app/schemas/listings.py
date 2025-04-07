from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

class ListingCreate(BaseModel):
    description: str
    price: Decimal = Field(..., gt=0)
    property_type_id: int  
    city: str
    street: str
    house_number: int = Field(..., gt=0)
    apartment_number: int = Field(..., gt=0)
    area: Decimal = Field(..., gt=0)
    rooms: int = Field(..., ge=0)
    bathrooms: int = Field(..., ge=0)
    latitude: Optional[Decimal] = Field(None, ge=-90, le=90)   
    longitude: Optional[Decimal] = Field(None, ge=-180, le=180) 
    category_ids: Optional[List[int]] = []  

class SavedListingCreate(BaseModel):
    listing_id: int

class SavedListingResponse(BaseModel):
    saved_id: int
    listing_id: int

    class Config:
        orm_mode = True

class PhotoResponse(BaseModel):
    photo_id: int
    photo_url: str

class PropertyTypeResponse(BaseModel):
    property_type_id: int
    name: str

    class Config:
        orm_mode = True

class CategoryResponse(BaseModel):
    category_id: int
    name: str

    class Config:
        orm_mode = True

class ListingResponse(BaseModel):
    listing_id: int
    user_id: int
    description: str
    price: Decimal
    property_type: PropertyTypeResponse  
    city: str
    street: str
    house_number: int
    apartment_number: Optional[int]
    area: Decimal
    rooms: int
    bathrooms: int
    latitude: Optional[Decimal]
    longitude: Optional[Decimal]
    created_at: datetime
    categories: List[CategoryResponse]  
    images: List[PhotoResponse] = []  

    class Config:
        orm_mode = True