from sqlalchemy.orm import Session
from app.db.models import Message
from app.schemas.messages import MessageCreate, MessageResponse, ChatResponse
from app.db.repositories.message_repository import (
    find_existing_chat,
    create_chat,
    create_message,
    get_chats_for_user,
    get_last_message_in_chat
)

def create_message_with_chat(db: Session, sender_id: int, ad_id: int, message_create: MessageCreate) -> Message:
    chat = find_existing_chat(db, sender_id, message_create.receiver_id)

    if not chat:
        chat = create_chat(db, sender_id, message_create.receiver_id)

    return create_message(db, sender_id, message_create.receiver_id, ad_id, message_create.message, chat.chat_id)

def fetch_user_chats(db: Session, user_id: int):
    chats = get_chats_for_user(db, user_id)

    if not chats:
        raise Exception("Чаты не найдены")

    chat_responses = []
    for chat in chats:
        last_message = get_last_message_in_chat(db, chat.chat_id)

        if last_message:
            last_message_response = MessageResponse(
                message_id=last_message.message_id,
                sender_id=last_message.sender_id,
                receiver_id=last_message.receiver_id,
                listing_id=last_message.listing_id,
                message=last_message.message,
                sent_at=last_message.sent_at
            )

        chat_responses.append(ChatResponse(
            chat_id=chat.chat_id,
            user_1_id=chat.user_1_id,
            user_2_id=chat.user_2_id,
            created_at=chat.created_at,
            last_message=last_message_response
        ))

    return chat_responses
