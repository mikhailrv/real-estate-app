from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.db.repositories.user_repository import update_user
from app.schemas.users import UserUpdate
from app.services.auth_service import get_current_user


def update_user_data(
    user_update: UserUpdate,  
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)

    return update_user(current_user, db)