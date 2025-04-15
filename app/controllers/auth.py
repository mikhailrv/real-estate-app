from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.users import LoginData, UserCreate
from app.services.auth_service import register_new_user, authenticate_user
from app.core.security import create_access_token
from app.db.database import get_db
from datetime import timedelta
from app.core.config import settings

router = APIRouter(
    tags=["Authorization"]
)

@router.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    register_new_user(user, db)
    return {"msg": "User created successfully"}


@router.post("/login/")
def login_user(data: LoginData, db: Session = Depends(get_db)):
    user = authenticate_user(data.email, data.password, db)
    access_token = create_access_token(
        data={"sub": str(user.user_id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

