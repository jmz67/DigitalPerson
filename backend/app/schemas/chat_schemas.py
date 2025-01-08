# app/schemas/chat_schemas.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PatientBase(BaseModel):
    name: str
    age: int
    department: str

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int

    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    patient_id: int

class ConversationCreate(ConversationBase):
    conversation_id: str
    pass

class Conversation(BaseModel):
    conversation_id: str
    patient_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    conversation_id: str
    sender: str  # 'user' 或 'assistant'
    text: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class ChatHistory(BaseModel):
    conversation_id: int
    messages: List[Message]