from sqlalchemy.orm import Session
from app.models import chat_models
from app.schemas import chat_schemas 

def get_patient(db: Session, patient_id: int):
    return db.query(chat_models.Patient).filter(chat_models.Patient.id == patient_id).first()
    
def create_patient(db: Session, patient: chat_schemas.PatientCreate):
    db_patient = chat_models.Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient
    
from sqlalchemy.exc import IntegrityError

def create_conversation(db: Session, conversation: chat_schemas.ConversationCreate):
    # 检查是否存在相同的 conversation_id
    existing_conversation = db.query(chat_models.Conversation).filter_by(conversation_id=conversation.conversation_id).first()
    
    if existing_conversation is not None:
        # 如果存在相同的 conversation_id，可以选择返回已存在的对话或抛出异常
        return existing_conversation  # 或者 raise Exception("Conversation with this ID already exists.")
    
    try:
        # 创建新的 Conversation 实例
        db_conversation = chat_models.Conversation(**conversation.model_dump())
        db.add(db_conversation)
        db.commit()
        db.refresh(db_conversation)
        
        return db_conversation
    
    except IntegrityError as e:
        # 如果由于某种原因（如并发问题）导致违反唯一性约束，回滚事务并处理错误
        db.rollback()
        raise ValueError("Failed to create conversation due to a conflict.") from e

def get_conversation(db: Session, conversation_id: int):     
    return db.query(chat_models.Conversation).filter(chat_models.Conversation.conversation_id == conversation_id).first()  
    
def create_message(db: Session, message: chat_schemas.MessageCreate):     
    db_message = chat_models.Message(**message.model_dump())     
    db.add(db_message)     
    db.commit()     
    db.refresh(db_message)     
    return db_message  
    
def get_chat_history(db: Session, conversation_id: int):     
    return db.query(chat_models.Message).filter(chat_models.Message.conversation_id == conversation_id).order_by(chat_models.Message.timestamp.asc()).all()