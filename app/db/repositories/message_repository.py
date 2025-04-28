from sqlalchemy.orm import Session
from app.db.models import Chat, Listing, Message, User
from sqlalchemy import or_

def find_existing_chat(db: Session, user1_id: int, ad_id: int):
    user2_id=db.query(Listing).filter(Listing.listing_id == ad_id).first().user_id
    return db.query(Chat).filter(
        or_(
            (Chat.user_1_id == user1_id) & (Chat.user_2_id == user2_id),
            (Chat.user_1_id == user2_id) & (Chat.user_2_id == user1_id)
        )
    ).first()

def create_chat(db: Session, user1_id: int, ad_id: int):
    chat = Chat(user_1_id=user1_id, user_2_id=db.query(Listing).filter(Listing.listing_id == ad_id).first().user_id)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

def create_message(db: Session, sender_id: int, listing_id: int, message_text: str, chat_id: int):
    message = Message(
        sender_id=sender_id,
        receiver_id= db.query(Listing).filter(Listing.listing_id == listing_id).first().user_id,
        listing_id=listing_id,
        message=message_text,
        chat_id=chat_id,
        isRead = False
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_chats_for_user(db: Session, user_id: int):
    return db.query(Chat).filter(
        (Chat.user_1_id == user_id) | (Chat.user_2_id == user_id)).all()

def get_companion(db: Session, chat: Chat, user_id: int):
    companion_id = chat.user_2_id if chat.user_1_id == user_id else chat.user_1_id
    return db.query(User).filter(User.user_id == companion_id).first()

def get_last_message_in_chat(db: Session, chat_id: int):
    return db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.sent_at.desc()).first()

def get_messages_by_chat_id(db: Session, chat_id: int):
    return db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.sent_at).all()

def count_unread_messages(db: Session, chat_id: int, user_id: int):
    return db.query(Message).filter(
        Message.chat_id == chat_id,
        Message.receiver_id == user_id,
        Message.isRead == False
    ).count()

