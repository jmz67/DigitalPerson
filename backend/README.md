# 数字人业务后端

## 项目介绍

调用 dify 平台 API，实现数字人业务的后端服务。

## 开发指南

### 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI 应用入口
│   ├── models.py        # 数据模型
│   ├── schemas.py       # 数据验证和序列化模型
│   ├── services/        # 后端业务逻辑
│   │   └── chat_service.py   # 处理聊天相关逻辑
│   └── api/             # API 路由
│       └── chat.py      # 聊天 API 路由
├── config.py           # 配置文件
├── poetry.lock         # Poetry 锁文件
├── pyproject.toml      # Poetry 配置文件
├── requirements.txt    # （可选）依赖文件
├── Dockerfile          # Dockerfile（如果需要容器化）
└── README.md           # 项目说明文档
```

### 初始化项目

我们将创建一个新的 python 环境并使用 poetry 管理依赖。

首先请确保我们已经安装了 poetry，如果没有，请参考官方文档安装。

进入项目目录，初始化 poetry 项目：

```
poetry new backend 
cd backend
```

当我们运行 `poetry new backend` 命令时，我们会创建一个新的项目，同时 poetry 会自动为我们设置一个新的虚拟环境。一样，如果我们在一个已经存在的项目中使用 `poetry add` 命令来添加依赖项，而该项目还没有被 poetry 初始化过，poetry 也会自动为这个项目创建一个新的虚拟环境。

```
poetry add fastapi uvicorn
poetry add requests  # 我们需要与外部 API 通信
poetry add pydantic  # 用于数据验证
```

### 添加配置文件

在项目根目录下面创建 `config.py` 用于存放配置：

```python   
import os

class Config:
    # 您的大模型 API 配置
    MODEL_API_URL = os.getenv('MODEL_API_URL', 'http://47.99.172.64:23016/v1/chat-messages')
    MODEL_API_KEY = os.getenv('MODEL_API_KEY', 'app-GvYaVF4fAB1N0MnShOMqXxW6')
```

### 创建服务逻辑

我们将把业务逻辑封装进入服务层，以保持我们的控制器（API 路由）干净整洁。

```python
import requests
import json
import re
from app.config import Config


class ChatService:
    @staticmethod
    def process_chat_message(message: str, conversation_id: str = None):
        """
        调用 dify 接口，解析返回数据
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
            "Authorization": f"Bearer {Config.LLM_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(Config.LLM_API_URL, json=payload, headers=headers)
            response.raise_for_status()

            doctor_question = None
            recommendation_texts = []
            new_conversation_id = conversation_id

            for line in response.text.split('\n'):
                if line.startswith('data: '):
                    try:
                        json_data = json.loads(line[6:])
                        if json_data.get('event') == 'node_finished' and json_data.get('data', {}).get(
                                'title') == '症状问题推荐答案':
                            text = json_data['data']['outputs']['text']
                            list_items = re.findall(r'(\d+\.\s+.*?)(?=\n\d+\.|\n$)', text, re.DOTALL)
                            if list_items:
                                recommendation_texts = [item.lstrip('0123456789. ').strip() for item in list_items]

                        if json_data.get('event') == 'workflow_finished':
                            doctor_question = json_data['data']['outputs']['answer']

                        if json_data.get('conversation_id'):
                            new_conversation_id = json_data['conversation_id']

                    except Exception as e:
                        print(f"Error parsing line: {e}")

            return doctor_question, recommendation_texts, new_conversation_id

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling the API: {e}")
```

### 创建 API 路由

```python
# /app/api/chat.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chat_service import ChatService

router = APIRouter()


# 定义请求体的数据结构
# 未来如果请求体多了，可以扩充为文件夹
class ChatMessageRequest(BaseModel):
    message: str
    conversation_id: str = None

# POST /chatMessage


@router.post("/chatMessage")
async def chat_message(request: ChatMessageRequest):
    try:
        doctor_question, recommendation_texts, new_conversation_id = ChatService.process_chat_message(
            request.message, request.conversation_id)
        return {
            'doctor_question': doctor_question,
            'recommendation_texts': recommendation_texts,
            'conversation_id': new_conversation_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 创建 FastAPI 应用入口

```python
# app/main.py

from fastapi import FastAPI
from app.api.chat import router as chat_router

app = FastAPI()

app.include_router(chat_router)

if __name__ == "__main__":
    import uvicorn 

    uvicorn.run(app, host="127.0.0.1", port=8080, reload=True)
```


