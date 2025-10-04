from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models import User
from app.db.database import get_db
from app.services.auth_service import get_current_user
from app.schemas.messages import ChatIdResponse, ChatResponse, MessageCreate, MessageResponse
from app.services.message_service import create_message_with_chat, fetch_messages_for_chat, fetch_user_chats
from app.db.repositories.message_repository import create_chat, create_message, find_existing_chat

router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)
# переделать
@router.post("/{chat_id}/", response_model=MessageResponse)
def send_message(
    chat_id: int,
    message_create: MessageCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return create_message_with_chat(db, user.user_id, chat_id, message_create)
# переделать
@router.post("/listing/{ad_id}/", response_model=MessageResponse)
def create_chat_and_send_message(
    ad_id: int,
    message_create: MessageCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    chat = create_chat(db, user.user_id, ad_id)
    return create_message(db, user.user_id, ad_id, message_create.message, chat.chat_id)

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

# переделать
@router.post("/chat_by_listing/{listing_id}/", response_model=ChatIdResponse) 
def get_or_create_chat_by_listing(
    listing_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    chat = find_existing_chat(db, user.user_id, listing_id)
    if not chat:
        chat = create_chat(db, user.user_id, listing_id)
    return {"chat_id": chat.chat_id}
