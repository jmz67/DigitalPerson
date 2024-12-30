
import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
import logging

from app.services.chat_service import ChatService
from app.config import Config

logger = logging.getLogger("app.api.chat")

router = APIRouter()

# 定义请求体的数据结构
class ChatMessageRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    sid: Optional[str] = None

# 依赖注入配置和服务
# 定义依赖函数
def get_config() -> Config:
    config_instance = Config()
    print(f"Config instance created: {config_instance.__dict__}")
    return config_instance

def get_chat_service(config: Config = Depends(get_config)) -> ChatService:
    print(f"ChatService received config: {config.__dict__}")
    return ChatService(config)

# POST /chatMessage
@router.post("/chatMessage")
async def chat_message(
    request: ChatMessageRequest,
    background_tasks: BackgroundTasks,
    chat_service: ChatService = Depends(get_chat_service)
):
    logger.info("Received chat message request")
    logger.debug(f"Request data: {request.model_dump_json()}")

    try:
        doctor_question, chat_type, recommendation_texts, new_conversation_id = await chat_service.process_chat_message(
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
