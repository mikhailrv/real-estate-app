from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    message: str

class MessageResponse(BaseModel):
    message_id: int
    sender_id: int
    receiver_id: int
    listing_id: int
    message: str
    sent_at: datetime

    class Config:
        orm_mode = True

class ChatCreate(BaseModel):
    user_1_id: int
    user_2_id: int

class CompanionResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

class ChatResponse(BaseModel):
    chat_id: int
    user_1_id: int
    user_2_id: int
    created_at: datetime
    last_message: MessageResponse
    companion: CompanionResponse

    class Config:
        orm_mode = True

