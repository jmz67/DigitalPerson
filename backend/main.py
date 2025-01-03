from fastapi import FastAPI, Depends
import logging

from app.logging_config import setup_logging
from app.config import Config
from app.api.v1.chat import router as chat_v1_router
from app.api.v2.chat import router as chat_v2_router
from app.services.chat_service import ChatService

app = FastAPI(title="Chat API")

# 设置日志
setup_logging()
logger = logging.getLogger("app.main")

# 依赖注入配置和服务
def get_config() -> Config:
    return Config()

def get_chat_service_instance(config: Config = Depends(get_config)) -> ChatService:
    return ChatService(config)

# 依赖注入连接池管理
@app.on_event("startup")
async def startup_event():
    logger.info("Application startup: Initializing resources")

@app.on_event("shutdown")
async def shutdown_event(chat_service: ChatService = Depends(get_chat_service_instance)):
    logger.info("Application shutdown: Closing resources")
    await chat_service.client.aclose()

# 包含路由
app.include_router(chat_v1_router)
app.include_router(chat_v2_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)
