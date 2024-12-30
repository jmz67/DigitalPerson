import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv('../.env')

class Config:
    def __init__(self):
        self.llm_api_url = os.getenv("LLM_API_URL", "http://47.99.172.64:23016/v1/chat-messages")
        self.llm_api_key = os.getenv("LLM_API_KEY", "app-xfLxo5sXKYs4eEf2Zg7kVvyc")
        self.push_structured_text_url = os.getenv("PUSH_STRUCTURED_TEXT_URL", "http://117.50.189.233:47061/api/digital_human_backend/push_structured_text")

# 使用配置
config = Config()

if __name__ == '__main__':

    print(config.llm_api_url)
