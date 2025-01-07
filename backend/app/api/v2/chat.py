import re
import uuid
import requests  # 如果需要异步调用，请用 httpx 或 aiohttp
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
import logging

from app.services.chat_service import ChatService
from app.config import Config

logger = logging.getLogger("app.api.chat_v2")

router = APIRouter(prefix="/v2")

class ChatMessageRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    sid: Optional[str] = None

def get_config() -> Config:
    return Config()

def get_chat_service(config: Config = Depends(get_config)) -> ChatService:
    return ChatService(config)

@router.post("/chatMessage")
async def chat_message_v2(
    request: ChatMessageRequest,
    background_tasks: BackgroundTasks,
    chat_service: ChatService = Depends(get_chat_service),
):
    """
    新的 v2 接口：先调用外部接口 http://47.99.172.64:23016/v1/chat-messages，
    拿到结果后，再进行定制化的结构化处理，返回给前端。
    """
    logger.info("Received chat message request (v2)")
    try:
        # 1. 组织请求体数据（外部接口需要的格式）
        post_data = {
            "inputs": {},
            "query": request.message,                 # 用前端传来的 message
            "response_mode": "blocking",
            "conversation_id": request.conversation_id or "",
            "user": "abc-123",                       # 看你业务需求，传固定或自定义
            "files": [],
        }

        # 2. 调用外部接口
        url = "http://47.99.172.64:23016/v1/chat-messages"
        headers = {
            "Authorization": "Bearer app-ZpkC6eatzXmILEJocQDqQWye"
        }
        
        resp = requests.post(url, json=post_data, headers=headers, timeout=15)
        if resp.status_code != 200:
            logger.error(f"外部接口返回非 200 状态码: {resp.status_code}")
            raise HTTPException(status_code=resp.status_code, detail=f"外部接口错误: {resp.text}")

        result = resp.json()

        """
        预期返回值示例（简化）:
        {
            "event": "message",
            "conversation_id": "398b327d-cdc0-43bd-bd6c-5783e607382b",
            "answer": "问题：皮肤哪里不舒服？\n推荐回答：1. 脸部 2. 手臂 3. 大腿 4. 其他？",
            "metadata": { ... },
            ...
        }
        """

        # 3. 从 result 中解析出 doctor_question, recommendation_texts, conversation_id 等
        # 解析 answer 字段
        answer_text = result.get("answer", "")

        # 提取 doctor_question
        doctor_question_match = re.search(r"问题：(.*?)(?=\n推荐回答：)", answer_text)
        doctor_question = doctor_question_match.group(1).strip() if doctor_question_match else ""

        # 提取 recommendation_texts
        recommendation_texts_match = re.search(r"推荐回答：(.*?)(?=\n|$)", answer_text)
        recommendation_texts_raw = recommendation_texts_match.group(1).strip() if recommendation_texts_match else ""
        recommendation_texts = re.findall(r"\d+\.\s*([^0-9]+)", recommendation_texts_raw)

        # 提取 chat_type
        chat_type_match = re.search(r"chat_type:\s*(\w+)", answer_text)
        chat_type = chat_type_match.group(1).strip() if chat_type_match else "unknown"

        # 提取 conversation_id
        conversation_id = result.get("conversation_id", "")

        # 构造最终的 response_data
        response_data = {
            "doctor_question": doctor_question,
            "chat_type": chat_type,
            "recommendation_texts": recommendation_texts,
            "conversation_id": conversation_id,
        }

        return response_data

    except Exception as e:
        logger.error(f"Error in chat_message_v2: {e}")
        raise HTTPException(status_code=500, detail=str(e))
