import json
import re
import uuid
import httpx
from typing import Optional, Tuple, List
import logging
import asyncio

from app.config import Config
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger("app.services.chat_service")

# 定义自定义异常以便重试
class TemporaryAPIError(Exception):
    pass

class ChatService:
    def __init__(self, config: Config):
        self.config = config
        # 配置 AsyncClient，提高连接池大小和超时时间
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(10.0, read=30.0),
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
            http2=True  # 启用 HTTP/2 以提高性能（前提是服务器支持）
        )

    def _is_retryable_exception(self, exception: Exception) -> bool:
        """判断异常是否为可重试的类型"""
        return isinstance(exception, (httpx.RequestError, TemporaryAPIError))

    # 使用 tenacity 装饰器为 process_chat_message 添加重试机制
    @retry(
        retry=retry_if_exception_type((httpx.RequestError, TemporaryAPIError)),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def process_chat_message_v1(
        self, 
        message: str, 
        conversation_id: Optional[str] = None
    ) -> Tuple[Optional[str], Optional[str], List[str], Optional[str]]:
        """
        调用 dify 接口，解析返回数据，并添加重试机制
        """
        payload = {
            "inputs": [],
            "query": message,
            "response_mode": "streaming",
            "user": "admin",
            "files": []
        }

        if conversation_id:
            payload["conversation_id"] = conversation_id

        headers = {
            "Authorization": f"Bearer {self.config.llm_api_key}",
            "Content-Type": "application/json"
        }

        try:
            logger.info("Processing chat message")
            logger.debug(f"Model API URL: {self.config.llm_api_url}")
            logger.debug(f"Payload: {json.dumps(payload, ensure_ascii=False)}")
            logger.debug(f"Headers: {json.dumps(headers, ensure_ascii=False)}")

            response = await self.client.post(self.config.llm_api_url, json=payload, headers=headers)

            logger.info(f"Received response: {response}")
            
            if response.status_code >= 500:
                # 对于服务器错误，抛出自定义异常以触发重试
                raise TemporaryAPIError(f"Server error: {response.status_code}")

            response.raise_for_status()

            doctor_question = None
            chat_type = None
            recommendation_texts = []
            new_conversation_id = conversation_id

            for line in response.text.split('\n'):
                if line.startswith('data: '):
                    try:
                        json_data = json.loads(line[6:])
                        if json_data.get('event') == 'node_finished':
                            
                            if json_data.get('data', {}).get('title') == '推荐答案':
                                text = json_data['data']['outputs']['text']
                                list_items = re.findall(r'(\d+\.\s+.*?)(?=\n\d+\.|\n$)', text, re.DOTALL)
                                if list_items:
                                    recommendation_texts = [item.lstrip('0123456789. ').strip() for item in list_items]
                                    logger.debug(f"Extracted recommendation texts: {recommendation_texts}")
                            if json_data.get('data', {}).get('title') == '对话状态':
                                chat_type = json_data['data']['inputs']['value']
                                logger.debug(f"Extracted chat_type: {chat_type}")

                        if json_data.get('event') == 'workflow_finished':
                            doctor_question = json_data['data']['outputs']['answer']
                            logger.debug(f"Extracted doctor question: {doctor_question}")

                        if json_data.get('conversation_id'):
                            new_conversation_id = json_data['conversation_id']
                            logger.debug(f"Updated conversation ID: {new_conversation_id}")

                    except json.JSONDecodeError as e:
                        logger.error(f"JSON decode error: {e}")
                    except Exception as e:
                        logger.error(f"Error parsing line: {e}")

            logger.info("Chat message processed successfully")
            return doctor_question, chat_type, recommendation_texts, new_conversation_id

        except (httpx.RequestError, TemporaryAPIError) as e:
            logger.error(f"Error calling the API: {e}")
            raise

    
    async def process_chat_message_v2(
        self, 
        message: str, 
        conversation_id: Optional[str] = None
    ) -> Tuple[Optional[str], Optional[str], List[str], Optional[str]]:
        """
        调用外部接口，解析返回数据，并添加重试机制
        """
        payload = {
            "inputs": {},
            "query": message,  # 用前端传来的 message
            "response_mode": "blocking",
            "conversation_id": conversation_id or "",
            "user": "abc-123",
            "files": [],
        }

        headers = {
            "Authorization": "Bearer app-ZpkC6eatzXmILEJocQDqQWye",
            "Content-Type": "application/json"
        }

        try:
            logger.info("Processing chat message (v2)")
            logger.debug(f"External API URL: http://47.99.172.64:23016/v1/chat-messages")
            logger.debug(f"Payload: {json.dumps(payload, ensure_ascii=False)}")
            logger.debug(f"Headers: {json.dumps(headers, ensure_ascii=False)}")

            # 调用外部接口
            response = await self.client.post(
                "http://47.99.172.64:23016/v1/chat-messages",
                json=payload,
                headers=headers
            )

            logger.info(f"Received response: {response}")

            if response.status_code >= 500:
                # 对于服务器错误，抛出自定义异常以触发重试
                raise TemporaryAPIError(f"Server error: {response.status_code}")

            response.raise_for_status()

            # 解析返回结果
            result = response.json()
            logger.debug(f"Response JSON: {json.dumps(result, ensure_ascii=False, indent=2)}")

            # 获取 answer 字段
            answer_text = result.get("answer", "").strip()

            # 提取 doctor_question
            doctor_question = ""
            doctor_question_match = re.search(r"问题：(.*?)(?=\n推荐回答：|\Z)", answer_text, re.S)
            if doctor_question_match:
                doctor_question = doctor_question_match.group(1).strip()

            # 提取 recommendation_texts
            recommendation_texts = []
            recommendation_texts_match = re.search(r"推荐回答：(.*?)(?=\n|$)", answer_text, re.S)
            if recommendation_texts_match:
                recommendation_texts_raw = recommendation_texts_match.group(1).strip()
                recommendation_texts = re.findall(r"\d+\.\s*([^0-9]+)", recommendation_texts_raw)

            # 提取 chat_type
            chat_type = "unknown"
            chat_type_match = re.search(r"chat_type:\s*(\w+)", answer_text)
            if chat_type_match:
                chat_type = chat_type_match.group(1).strip()

            # 提取 conversation_id
            new_conversation_id = result.get("conversation_id", "")

            logger.info(
                f"解析结果: doctor_question={doctor_question}, "
                f"recommendation_texts={recommendation_texts}, "
                f"chat_type={chat_type}, "
                f"conversation_id={new_conversation_id}"
            )

            return doctor_question, chat_type, recommendation_texts, new_conversation_id

        except (httpx.RequestError, TemporaryAPIError) as e:
            logger.error(f"Error calling the API: {e}")
            raise
    
    # 使用 tenacity 装饰器为 push_structured_text 添加重试机制
    @retry(
        retry=retry_if_exception_type((httpx.RequestError, TemporaryAPIError)),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def push_structured_text(self, text_id: str, content: str, sid: str):
        """
        将结构化的文本推送到指定后端服务，并打印响应结果，同时添加重试机制
        """
        url = self.config.push_structured_text_url
        headers = {'Content-Type': 'application/json'}
        data = {
            "text_id": text_id,
            "sid": sid,
            "structured_text": {
                "content": content
            }
        }
        try:
            logger.info(f"Pushing structured text with text_id: {text_id}")
            response = await self.client.post(url, headers=headers, json=data, timeout=10.0)
            
            if response.status_code >= 500:
                # 对于服务器错误，抛出自定义异常以触发重试
                raise TemporaryAPIError(f"Server error: {response.status_code}")

            response.raise_for_status()
            # 打印响应状态码和内容
            logger.info(f"Structured text pushed successfully with text_id: {text_id}")
            logger.debug(f"Response Status Code: {response.status_code}")
            try:
                response_json = response.json()
                logger.debug(f"Response JSON: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
            except json.JSONDecodeError:
                # 如果响应不是JSON格式，打印原始文本
                logger.debug(f"Response Text: {response.text}")
        except (httpx.RequestError, TemporaryAPIError) as e:
            logger.error(f"Error pushing structured text with text_id {text_id}: {e}")
            raise

    async def close(self):
        """确保 AsyncClient 正确关闭以释放资源"""
        await self.client.aclose()
