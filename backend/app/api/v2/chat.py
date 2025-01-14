import re
import uuid
import requests  # 如果需要异步调用，请用 httpx 或 aiohttp
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
import logging

from app.config import Config
from app.services.chat_service import ChatService

from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),  # 最多重试3次
    wait=wait_fixed(2),          # 每次重试间隔2秒
    retry=retry_if_exception_type(requests.exceptions.RequestException),  # 仅在网络请求异常时重试
)
def call_external_api(url: str, headers: dict, post_data: dict, timeout: int = 15):
    """
    调用外部API，并处理重试逻辑
    """
    logger.info(f"调用大模型接口: {url}, post_data: {post_data}")
    resp = requests.post(url, json=post_data, headers=headers, timeout=timeout)
    if resp.status_code != 200:
        logger.error(f"外部接口返回非 200 状态码: {resp.status_code}")
        raise HTTPException(status_code=resp.status_code, detail=f"外部接口错误: {resp.text}")
    return resp.json()

logger = logging.getLogger("app.api.chat_v2")

router = APIRouter(prefix="/v2")

class ChatMessageRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    sid: Optional[str] = None

def get_config() -> Config:
    return Config()

def get_chat_service(config: Config = Depends(get_config)) -> ChatService:
    print(f"ChatService received config: {config.__dict__}")
    return ChatService(config)

@router.post("/chatMessage")
async def chat_message(
    request: ChatMessageRequest,
    background_tasks: BackgroundTasks,
    chat_service: ChatService = Depends(get_chat_service)
):
    logger.info("Received chat message request")
    logger.debug(f"Request data: {request.model_dump_json()}")

    try:
        doctor_question, chat_type, recommendation_texts, new_conversation_id = await chat_service.process_chat_message_v2(
            request.message,
            request.conversation_id
        )

        # 使用 BackgroundTasks 进行后台处理
        if doctor_question:
            text_id = str(uuid.uuid4())  # 生成唯一的 text_id
            background_tasks.add_task(chat_service.push_structured_text, text_id, doctor_question, request.sid)
            logger.info(f"Added background task to push structured text with text_id: {text_id}")

        response_data = {
            'doctor_question': doctor_question,
            'chat_type': chat_type,
            'recommendation_texts': recommendation_texts,
            'conversation_id': new_conversation_id
        }
        logger.debug(f"Response data: {response_data}")
        return response_data
    except Exception as e:
        logger.error(f"Error processing chat message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, APIRouter
from app.models.chat_models import Conversation as ModelConversation, Message as ModelMessage  # 直接导入模型类
from app.schemas.chat_schemas import Conversation, ConversationCreate, Message, MessageCreate, ChatHistory  # 直接导入 Pydantic 模型
from app.services.chat_history import create_conversation, create_message, get_patient, get_conversation, get_chat_history  # 直接导入服务函数
from app.database import SessionLocal

# 依赖项，获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/createConversation", response_model=Conversation)
def createConversation(conversation: ConversationCreate, db: Session = Depends(get_db)):
    # # 可选：验证患者是否存在
    # patient = get_patient(db, conversation.patient_id)
    # if not patient:
    #     logger.error(f"Patient not found: {conversation.patient_id}")
    #     raise HTTPException(status_code=404, detail="Patient not found")
    return create_conversation(db, conversation)

@router.post("/saveMessage", response_model=Message)
def save_message(message: MessageCreate, db: Session = Depends(get_db)):
    # 验证 conversation_id 是否存在
    conversation = get_conversation(db, message.conversation_id)
    if not conversation:
        logger.error(f"Conversation not found: {message.conversation_id}")
        raise HTTPException(status_code=404, detail="Conversation not found")
    if message.sender not in ['user', 'assistant']:
        raise HTTPException(status_code=400, detail="Invalid sender")
    return create_message(db, message)

@router.get("/chatHistory/{conversation_id}", response_model=ChatHistory)
def get_chat_history(conversation_id: int, db: Session = Depends(get_db)):
    conversation = get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = get_chat_history(db, conversation_id)
    return ChatHistory(conversation_id=conversation_id, messages=messages)
