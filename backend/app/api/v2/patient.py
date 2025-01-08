from fastapi import APIRouter
import random
from datetime import datetime

router = APIRouter(prefix="/v2")

# 一个简单的辅助函数，用于生成随机的患者信息
# def generate_dynamic_patient_info():
#     return {
#         "id": random.randint(10000, 99999),  # 随机生成 ID
#         "name": f"Patient-{random.randint(1, 100)}",  # 随机生成姓名
#         "age": random.randint(18, 90),  # 随机生成年龄
#         "department": random.choice(["皮肤科", "内科", "外科", "眼科", "耳鼻喉科"]),  # 随机选择科室
#         # "conversation_id": datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3],  # 使用当前时间戳作为 conversation_id
#         "conversation_id": None,  # 使用当前时间戳作为 conversation_id
#         "timestamp": datetime.now().isoformat()  # 添加请求的时间戳
#     }

def generate_dynamic_patient_info():
    return {
        "id": 1,
        "name": "范德彪",
        "age": 30,
        "department": "内科",
        # "conversation_id": datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3],  # 使用当前时间戳作为 conversation_id
        "conversation_id": None,  
        "timestamp": datetime.now().isoformat()  # 添加请求的时间戳
    }

@router.get("/patientInfo")
def get_patient_info():
    # 调用辅助函数获取动态生成的患者信息
    patient_info = generate_dynamic_patient_info()
    return patient_info