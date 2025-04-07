from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.schemas.users import UserUpdate
from app.api.auth import get_current_user

router = APIRouter()

# работает
@router.get("/users/me/", response_model=UserUpdate)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# работает
@router.put("/users/me/", response_model=UserUpdate)
def update_me(
    user_update: UserUpdate,  
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return current_user