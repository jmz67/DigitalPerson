import re
import unittest

def parse_result(result):
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
    conversation_id = result.get("conversation_id", "")

    return {
        "doctor_question": doctor_question,
        "recommendation_texts": recommendation_texts,
        "chat_type": chat_type,
        "conversation_id": conversation_id,
    }

class TestParsingLogic(unittest.TestCase):
    def test_full_data(self):
        result = {
            "answer": (
                "问题：主诉：腿部有症状很久了三天左右，无伴随症状。\n\n"
                "现病史：患者自述腿部症状已经持续很久了三天左右，无明显加重或缓解，"
                "饮食方面偏好清淡食物，夜间睡眠质量较差，大便次数增多但未见异常，小便正常。\n\n"
                "推荐回答：1. 谢谢你医生！2. 好的，再见！"
            ),
            "conversation_id": "abc123"
        }
        expected_output = {
            "doctor_question": (
                "主诉：腿部有症状很久了三天左右，无伴随症状。\n\n"
                "现病史：患者自述腿部症状已经持续很久了三天左右，无明显加重或缓解，"
                "饮食方面偏好清淡食物，夜间睡眠质量较差，大便次数增多但未见异常，小便正常。"
            ),
            "recommendation_texts": ["谢谢你医生！", "好的，再见！"],
            "chat_type": "unknown",
            "conversation_id": "abc123",
        }
        self.assertEqual(parse_result(result), expected_output)

    def test_missing_recommendation(self):
        result = {
            "answer": (
                "问题：主诉：腿部有症状很久了三天左右，无伴随症状。\n\n"
                "现病史：患者自述腿部症状已经持续很久了三天左右，无明显加重或缓解，"
                "饮食方面偏好清淡食物，夜间睡眠质量较差，大便次数增多但未见异常，小便正常。\n\n"
            ),
            "conversation_id": "abc123"
        }
        expected_output = {
            "doctor_question": (
                "主诉：腿部有症状很久了三天左右，无伴随症状。\n\n"
                "现病史：患者自述腿部症状已经持续很久了三天左右，无明显加重或缓解，"
                "饮食方面偏好清淡食物，夜间睡眠质量较差，大便次数增多但未见异常，小便正常。"
            ),
            "recommendation_texts": [],
            "chat_type": "unknown",
            "conversation_id": "abc123",
        }
        self.assertEqual(parse_result(result), expected_output)

    def test_empty_answer(self):
        result = {
            "answer": "",
            "conversation_id": "xyz789"
        }
        expected_output = {
            "doctor_question": "",
            "recommendation_texts": [],
            "chat_type": "unknown",
            "conversation_id": "xyz789",
        }
        self.assertEqual(parse_result(result), expected_output)

if __name__ == "__main__":
    unittest.main()
