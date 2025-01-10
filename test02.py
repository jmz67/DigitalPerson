import json

def main(
    data: str, 
    condition_fields: list,
    history_fields: list,
    personal_fields: list
):
    # 将字段列表转换为字典，便于快速访问
    condition_dict = {item["field_name_eg"]: item for item in condition_fields}
    history_dict = {item["field_name_eg"]: item for item in history_fields}
    personal_dict = {item["field_name_eg"]: item for item in personal_fields}

    # 解析 JSON 数据
    try:
        data_dict = json.loads(data)
    except json.JSONDecodeError:
        raise ValueError("提供的数据不是有效的JSON格式")

    latest_record = data_dict.get("latestMedicalRecord", {})
    past_history = latest_record.get("pastHistory", {})
    basic_info = latest_record.get("basicInfo", {})
    marriage_child_info = latest_record.get("marriageChildInfo", {})
    allergy_history = latest_record.get("allergyHistory", "无")
    visit_info = data_dict.get("revisitInfo", {})
    last_record = visit_info.get("lastRecord", {})

    # 获取性别信息
    gender = basic_info.get("gender", "未知")

    # 处理 condition_fields
    condition_dict["treatment_visited"]["field_content"] = "是" if visit_info.get("isRevisit", False) else "否"
    condition_dict["treatment_diagnosis"]["field_content"] = last_record.get("diagnosis", {}).get("westernDiagnosisName")

    # 处理 history_fields
    disease_history = past_history.get("diseaseHistory")
    if disease_history:
        history_dict["chronic_disease_present"]["field_content"] = "有"
        history_dict["chronic_disease_name"]["field_content"] = disease_history

    # 传染病史
    infectious_history = past_history.get("infectiousDiseaseHistory")
    if infectious_history and isinstance(infectious_history, dict):
        history_dict["infectious_disease_present"]["field_content"] = "有"
        history_dict["infectious_disease_name"]["field_content"] = infectious_history.get("diseaseName")
        history_dict["infectious_disease_treatment"]["field_content"] = infectious_history.get("treatment")

    # 手术史
    surgery_history = past_history.get("surgeryHistory")
    if surgery_history and surgery_history != "无":
        history_dict["surgery_present"]["field_content"] = "有"
        surgery_name = past_history.get("surgeryName")
        if surgery_name:
            history_dict["surgery_name"]["field_content"] = surgery_name
        surgery_time = past_history.get("surgeryTime")
        if surgery_time:
            history_dict["surgery_time"]["field_content"] = surgery_time
        surgery_medical_institution = past_history.get("surgeryMedicalInstitution")
        if surgery_medical_institution:
            history_dict["surgery_medical_institution"]["field_content"] = surgery_medical_institution

    # 处理 personal_fields
    # 这里只处理性别，其他字段按需处理
    personal_dict["gender"]["field_content"] = gender

    # 收集关键赋值字段
    key_fields = {}

    # 从 condition_fields 提取
    key_fields["treatment_visited"] = condition_dict.get("treatment_visited", {}).get("field_content")
    key_fields["treatment_diagnosis"] = condition_dict.get("treatment_diagnosis", {}).get("field_content")

    # 从 history_fields 提取
    key_fields["infectious_disease_present"] = history_dict.get("infectious_disease_present", {}).get("field_content")
    key_fields["infectious_disease_name"] = history_dict.get("infectious_disease_name", {}).get("field_content")
    key_fields["infectious_disease_treatment"] = history_dict.get("infectious_disease_treatment", {}).get("field_content")
    key_fields["surgery_name"] = history_dict.get("surgery_name", {}).get("field_content")
    key_fields["surgery_time"] = history_dict.get("surgery_time", {}).get("field_content")
    key_fields["surgery_medical_institution"] = history_dict.get("surgery_medical_institution", {}).get("field_content")

    # 从 personal_fields 提取
    key_fields["gender"] = personal_dict.get("gender", {}).get("field_content")

    # 返回包含三个对象和所有关键赋值字段的字典
    return {
        "condition_fields": condition_fields,
        "history_fields": history_fields,
        "personal_fields": personal_fields,

        "treatment_visited": key_fields.get("treatment_visited"),
        "treatment_diagnosis": key_fields.get("treatment_diagnosis"),

        "infectious_disease_present": key_fields.get("infectious_disease_present"),
        "infectious_disease_name": key_fields.get("infectious_disease_name"),
        "infectious_disease_treatment": key_fields.get("infectious_disease_treatment"),

        "surgery_name": key_fields.get("surgery_name"),
        "surgery_time": key_fields.get("surgery_time"),
        "surgery_medical_institution": key_fields.get("surgery_medical_institution"),
        
        "gender": key_fields.get("gender")
    }
