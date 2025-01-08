# app/models/chat_models.py

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship 
from sqlalchemy.sql import func 
from app.database import Base

class Patient(Base):     
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)     
    name = Column(String(256), index=True)     
    age = Column(Integer)     
    department = Column(String(256), index=True)      
    conversations = relationship("Conversation", back_populates="patient")

class Conversation(Base):
    __tablename__ = "conversations"

    conversation_id = Column(String(256), primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(256), ForeignKey("conversations.conversation_id"), nullable=False)
    sender = Column(String(256), nullable=False)  # 'user' 或 'assistant'
    text = Column(String(256), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    conversation = relationship("Conversation", back_populates="messages")