from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models import User
from app.db.database import get_db
from app.services.auth_service import get_current_user
from app.schemas.messages import ChatResponse, MessageCreate, MessageResponse
from app.services.message_service import create_message_with_chat, fetch_messages_for_chat, fetch_user_chats

router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)

@router.post("/{ad_id}/", response_model=MessageResponse)
def send_message(
    ad_id: int,
    message_create: MessageCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return create_message_with_chat(db, user.user_id, ad_id, message_create)

@router.get("/chats/", response_model=List[ChatResponse])
def get_dialogs(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    chats = fetch_user_chats(db, user.user_id)
    if not chats:
        raise HTTPException(status_code=404, detail="Чаты не найдены")
    return chats

@router.get("/{chat_id}/", response_model=List[MessageResponse])
def get_messages(chat_id: int, db: Session = Depends(get_db), user: User = (Depends(get_current_user))):
    messages = fetch_messages_for_chat(db, chat_id, user)
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for this chat")
    return messages