from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.repositories.user_repository import get_user_by_email, create_user, get_user_by_id
from app.schemas.users import UserCreate
from app.core.security import hash_password, verify_password, oauth2_scheme
from app.core.config import settings
from jose import JWTError, jwt

def register_new_user(user_data: UserCreate, db: Session):
    existing_user = get_user_by_email(user_data.email, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )

    hashed = hash_password(user_data.password)

    create_user(
        db=db,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=hashed
    )


def authenticate_user(email: str, password: str, db: Session):
    user = get_user_by_email(email, db)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_id(user_id, db)

    if user is None:
        raise credentials_exception 
    
    return user




