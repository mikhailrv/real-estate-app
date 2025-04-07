from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(..., max_length=100)

class CategoryResponse(BaseModel):
    category_id: int
    name: str

    class Config:
        orm_mode = True

