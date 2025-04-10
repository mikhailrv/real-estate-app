from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.users import UserUpdate


def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(user_id: int, db: Session):
    return db.query(User).filter(User.user_id == user_id).first()

def create_user(db: Session, first_name: str, last_name: str, email: str, phone: str, password_hash: str):
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        password_hash=password_hash
    )
    db.add(user)
    db.commit()
    return user

def update_user(db: Session, user: UserUpdate):
    db.commit()
    db.refresh(user)
    return user
