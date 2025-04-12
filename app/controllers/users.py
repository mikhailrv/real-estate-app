from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.schemas.users import UserUpdate
from app.services.auth_service import get_current_user
from app.services.user_service import update_user_data

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me/", response_model=UserUpdate)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me/", response_model=UserUpdate)
def update_me(
    user_update: UserUpdate,  
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    
    update_user_data(user_update, db, current_user)

    return current_user