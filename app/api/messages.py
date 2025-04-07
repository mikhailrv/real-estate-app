from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models import Chat, Message, User
from app.db.database import get_db
from app.api.auth import get_current_user
from app.schemas.messages import ChatResponse, MessageCreate, MessageResponse

router = APIRouter()

# работает 
@router.post("/messages/{ad_id}/", response_model=MessageResponse)
def send_message(ad_id: int, message_create: MessageCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    chat = db.query(Chat).filter(
        (Chat.user_1_id == user.user_id and Chat.user_2_id == message_create.receiver_id) |
        (Chat.user_1_id == message_create.receiver_id and Chat.user_2_id == user.user_id)
    ).first()

    if not chat:
        chat = Chat(user_1_id=user.user_id, user_2_id=message_create.receiver_id)
        db.add(chat)
        db.commit()
        db.refresh(chat)

    message = Message(
        sender_id=user.user_id,
        receiver_id=message_create.receiver_id,
        listing_id=ad_id,  
        message=message_create.message,
        chat_id=chat.chat_id  
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message



@router.get("/chats/", response_model=List[ChatResponse])
def get_dialogs(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Получаем все чаты, в которых участвует пользователь
    chats = db.query(Chat).filter(
        (Chat.user_1_id == user.user_id) | (Chat.user_2_id == user.user_id)
    ).all()

    if not chats:
        raise HTTPException(status_code=404, detail="Чаты не найдены")

    chat_responses = []
    for chat in chats:

        last_message = db.query(Message).filter(Message.chat_id == chat.chat_id).order_by(Message.sent_at.desc()).first()

        last_message_response = None
        if last_message:
            last_message_response = MessageResponse(
                message_id=last_message.message_id,
                sender_id=last_message.sender_id,
                receiver_id=last_message.receiver_id,
                listing_id=last_message.listing_id,
                message=last_message.message,
                sent_at=last_message.sent_at
            )

        chat_responses.append(
            ChatResponse(
                chat_id=chat.chat_id,
                user_1_id=chat.user_1_id,
                user_2_id=chat.user_2_id,
                created_at=chat.created_at,
                last_message=last_message_response 
            )
        )

    return chat_responses


