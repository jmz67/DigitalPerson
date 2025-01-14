from fastapi import FastAPI, Depends
import logging
from app.logging_config import setup_logging
from app.config import Config
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.chat import router as chat_v1_router
from app.api.v2.chat import router as chat_v2_router
from app.api.v2.auth import router as auth_router
from app.api.v2.patient import router as patient_router
from app.services.chat_service import ChatService

# 设置日志
setup_logging()
logger = logging.getLogger("app.main")

app = FastAPI(title="Chat API")

origins = [
    "http://localhost",
    "http://localhost:5178",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 或 ["*"] 允许所有来源（开发）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 依赖注入配置和服务
def get_config() -> Config:
    return Config()

def get_chat_service_instance(config: Config = Depends(get_config)) -> ChatService:
    return ChatService(config)

@app.on_event("startup")
async def startup_event():
    from app.database import Base, engine
    Base.metadata.create_all(bind=engine)  # 移动到这里，确保总是执行
    logger.info("Application startup: Initializing resources")

@app.on_event("shutdown")
async def shutdown_event(chat_service: ChatService = Depends(get_chat_service_instance)):
    logger.info("Application shutdown: Closing resources")
    await chat_service.client.aclose()

# 包含路由
app.include_router(chat_v1_router)
app.include_router(chat_v2_router)
app.include_router(auth_router)
app.include_router(patient_router)

if __name__ == "__main__":
    import uvicorn
    
    # 生产环境下应从环境变量或配置文件读取host和port，并且不要使用reload=True
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)