import json

def get_nested_value(data_dict, path, default=None):
    """
    根据给定的路径从嵌套的字典中获取值。
    path 使用点分隔的字符串表示，如 "latestMedicalRecord.basicInfo.gender"
    """
    keys = path.split('.')
    current = data_dict
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

def main(data):
    # 定义初始的字段
    condition_fields = [
        {"field_name_eg": "condition", "field_name_cn": "基本症状", "field_content": None},
        {"field_name_eg": "condition_duration", "field_name_cn": "症状持续时间", "field_content": None},
        {"field_name_eg": "condition_location", "field_name_cn": "症状部位", "field_content": None},
        {"field_name_eg": "condition_severity", "field_name_cn": "症状严重程度", "field_content": None},
        {"field_name_eg": "associated_symptoms", "field_name_cn": "伴随症状", "field_content": None},
        {"field_name_eg": "treatment_visited", "field_name_cn": "有无就诊治疗过", "field_content": None},
        {"field_name_eg": "treatment_diagnosis", "field_name_cn": "就诊诊断", "field_content": None},
        {"field_name_eg": "treatment_self_medication", "field_name_cn": "有无自行使用过药物或者采取过其他治疗措施", "field_content": None},
        {"field_name_eg": "medication_name", "field_name_cn": "药物名称", "field_content": None},
        {"field_name_eg": "treatment_method_name", "field_name_cn": "治疗措施名称", "field_content": None},
    ]

    history_fields = [
        {"field_name_eg": "chronic_disease_present", "field_name_cn": "有无慢性疾病", "field_content": None},
        {"field_name_eg": "chronic_disease_name", "field_name_cn": "慢性疾病名称", "field_content": None},
        {"field_name_eg": "chronic_disease_diagnosis_time", "field_name_cn": "确诊时间", "field_content": None},
        {"field_name_eg": "infectious_disease_present", "field_name_cn": "有无传染病史", "field_content": None},
        {"field_name_eg": "infectious_disease_name", "field_name_cn": "疾病名称", "field_content": None},
        {"field_name_eg": "infectious_disease_treatment", "field_name_cn": "是否进行治疗", "field_content": None},
        {"field_name_eg": "allergy_present", "field_name_cn": "有无过敏食物或药物", "field_content": None},
        {"field_name_eg": "allergy_food_name", "field_name_cn": "过敏食物名称", "field_content": None},
        {"field_name_eg": "allergy_medication_name", "field_name_cn": "药物名称", "field_content": None},
        {"field_name_eg": "surgery_present", "field_name_cn": "有无手术史", "field_content": None},
        {"field_name_eg": "surgery_time", "field_name_cn": "手术时间", "field_content": None},
        {"field_name_eg": "surgery_name", "field_name_cn": "手术名称", "field_content": None},
        {"field_name_eg": "surgery_medical_institution", "field_name_cn": "手术医疗机构", "field_content": None},
        {"field_name_eg": "family_history_present", "field_name_cn": "家属有无相关家族史", "field_content": None},
        {"field_name_eg": "family_history_relative", "field_name_cn": "亲属关系", "field_content": None},
        {"field_name_eg": "family_history_disease", "field_name_cn": "疾病名称", "field_content": None},
        {"field_name_eg": "long_term_medication_present", "field_name_cn": "有无长期用药史", "field_content": None},
        {"field_name_eg": "long_term_medication_name", "field_name_cn": "长期用药名称", "field_content": None},
    ]

    personal_fields = [
        {"field_name_eg": "personal_history", "field_name_cn": "个人史", "field_content": None},
        {"field_name_eg": "personal_bad_habits", "field_name_cn": "是否有不良生活习惯", "field_content": None},
        {"field_name_eg": "personal_smoking", "field_name_cn": "是否抽烟", "field_content": None},
        {"field_name_eg": "personal_smoking_frequency", "field_name_cn": "抽烟频率", "field_content": None},
        {"field_name_eg": "personal_drinking", "field_name_cn": "是否喝酒", "field_content": None},
        {"field_name_eg": "personal_drinking_frequency", "field_name_cn": "喝酒频率", "field_content": None},
        {"field_name_eg": "personal_late_night", "field_name_cn": "是否经常熬夜", "field_content": None},
        {"field_name_eg": "dietary_status", "field_name_cn": "饮食与口味状况", "field_content": None},
        {"field_name_eg": "sleep_status", "field_name_cn": "睡眠状况", "field_content": None},
        {"field_name_eg": "bowel_movement", "field_name_cn": "大便状况", "field_content": None},
        {"field_name_eg": "urine_status", "field_name_cn": "小便状况", "field_content": None},
        {"field_name_eg": "menstrual_history", "field_name_cn": "月经史（18-55）", "field_content": None},
        {"field_name_eg": "menstrual_cycle", "field_name_cn": "月经周期", "field_content": None},
        {"field_name_eg": "menstrual_duration", "field_name_cn": "经期天数", "field_content": None},
        {"field_name_eg": "last_menstrual_period", "field_name_cn": "末次月经时间", "field_content": None},
        {"field_name_eg": "menstrual_flow", "field_name_cn": "经量", "field_content": None},
        {"field_name_eg": "menstrual_color", "field_name_cn": "经色", "field_content": None},
        {"field_name_eg": "menstrual_quality", "field_name_cn": "经质", "field_content": None},
        {"field_name_eg": "marital_reproductive_history", "field_name_cn": "婚育史（18周岁以上）", "field_content": None},
        {"field_name_eg": "marital_status", "field_name_cn": "是否已婚", "field_content": None},
        {"field_name_eg": "childbirth_status", "field_name_cn": "是否生育", "field_content": None},
        {"field_name_eg": "full_term_birth_count", "field_name_cn": "足月生产个数", "field_content": None},
        {"field_name_eg": "preterm_birth_count", "field_name_cn": "早产个数", "field_content": None},
        {"field_name_eg": "miscarriage_count", "field_name_cn": "流产个数", "field_content": None},
        {"field_name_eg": "living_children_count", "field_name_cn": "现存子女数量", "field_content": None},
        {"field_name_eg": "children_count", "field_name_cn": "已育子女数量", "field_content": None},
    ]

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
    # 基本症状相关字段留空，等待问答过程填充
    # 仅处理非基本症状相关字段
    condition_dict["treatment_visited"]["field_content"] = "是" if visit_info.get("isRevisit", False) else "否"
    condition_dict["treatment_diagnosis"]["field_content"] = last_record.get("diagnosis", {}).get("westernDiagnosisName")
    condition_dict["treatment_self_medication"]["field_content"] = last_record.get("treatmentAdvice")
    condition_dict["medication_name"]["field_content"] = last_record.get("prescription", {}).get("prescriptionName")
    condition_dict["treatment_method_name"]["field_content"] = last_record.get("treatmentPrinciple")

    # 处理 history_fields
    disease_history = past_history.get("diseaseHistory")
    if disease_history:
        history_dict["chronic_disease_present"]["field_content"] = "有"
        history_dict["chronic_disease_name"]["field_content"] = disease_history

    disease_diagnosis_time = past_history.get("diseaseDiagnosisTime")
    if disease_diagnosis_time:
        history_dict["chronic_disease_diagnosis_time"]["field_content"] = disease_diagnosis_time

    # 传染病史（假设JSON中有相关字段）
    infectious_history = past_history.get("infectiousDiseaseHistory")
    if infectious_history and isinstance(infectious_history, dict):
        history_dict["infectious_disease_present"]["field_content"] = "有"
        history_dict["infectious_disease_name"]["field_content"] = infectious_history.get("diseaseName")
        history_dict["infectious_disease_treatment"]["field_content"] = infectious_history.get("treatment")

    # 过敏史
    if allergy_history and allergy_history != "无":
        history_dict["allergy_present"]["field_content"] = "有"
        history_dict["allergy_medication_name"]["field_content"] = allergy_history
        # 如果有过敏食物名称，可以根据实际字段赋值
        allergy_food_name = past_history.get("allergyFoodName")
        if allergy_food_name:
            history_dict["allergy_food_name"]["field_content"] = allergy_food_name

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

    # 家族史
    family_history = past_history.get("familyHistory")
    if family_history and isinstance(family_history, dict):
        history_dict["family_history_present"]["field_content"] = "有"
        family_relative = family_history.get("relative")
        if family_relative:
            history_dict["family_history_relative"]["field_content"] = family_relative
        disease = family_history.get("disease")
        if disease:
            history_dict["family_history_disease"]["field_content"] = disease

    # 长期用药史
    long_term_medication = past_history.get("longTermMedicationHistory")
    if long_term_medication and isinstance(long_term_medication, dict):
        history_dict["long_term_medication_present"]["field_content"] = "有"
        medication_name = long_term_medication.get("medicationName")
        if medication_name:
            history_dict["long_term_medication_name"]["field_content"] = medication_name

    # 处理 personal_fields
    personal_history = past_history.get("personalHistory")
    if personal_history:
        personal_dict["personal_history"]["field_content"] = personal_history

    bad_habits = past_history.get("badHabits")
    if bad_habits:
        personal_dict["personal_bad_habits"]["field_content"] = bad_habits

    # 吸烟
    smoking = past_history.get("smoking")
    if smoking is not None:
        personal_dict["personal_smoking"]["field_content"] = "是" if smoking else "否"
        if smoking:
            smoking_freq = past_history.get("smokingFrequency")
            if smoking_freq:
                personal_dict["personal_smoking_frequency"]["field_content"] = smoking_freq

    # 喝酒
    drinking = past_history.get("drinking")
    if drinking is not None:
        personal_dict["personal_drinking"]["field_content"] = "是" if drinking else "否"
        if drinking:
            drinking_freq = past_history.get("drinkingFrequency")
            if drinking_freq:
                personal_dict["personal_drinking_frequency"]["field_content"] = drinking_freq

    # 熬夜
    late_night = past_history.get("lateNight")
    if late_night is not None:
        personal_dict["personal_late_night"]["field_content"] = "是" if late_night else "否"

    # 饮食与口味状况
    dietary_status = past_history.get("dietaryStatus")
    if dietary_status:
        personal_dict["dietary_status"]["field_content"] = dietary_status

    # 睡眠状况
    sleep_status = past_history.get("sleepStatus")
    if sleep_status:
        personal_dict["sleep_status"]["field_content"] = sleep_status

    # 大便状况
    bowel_movement = past_history.get("bowelMovement")
    if bowel_movement:
        personal_dict["bowel_movement"]["field_content"] = bowel_movement

    # 小便状况
    urine_status = past_history.get("urineStatus")
    if urine_status:
        personal_dict["urine_status"]["field_content"] = urine_status

    # 月经史相关（仅女性处理）
    if gender == "女":
        menstrual_history = past_history.get("menstrualHistory")
        if menstrual_history and isinstance(menstrual_history, dict):
            personal_dict["menstrual_history"]["field_content"] = "有"
            cycle = menstrual_history.get("intervalDays")
            if cycle:
                personal_dict["menstrual_cycle"]["field_content"] = cycle
            duration = menstrual_history.get("durationDays")
            if duration:
                personal_dict["menstrual_duration"]["field_content"] = duration
            last_period = menstrual_history.get("lastMenstrualDate")
            if last_period:
                personal_dict["last_menstrual_period"]["field_content"] = last_period
            menstrual_flow = menstrual_history.get("menstrualFlow")
            if menstrual_flow:
                personal_dict["menstrual_flow"]["field_content"] = menstrual_flow
            menstrual_color = menstrual_history.get("menstrualColor")
            if menstrual_color:
                personal_dict["menstrual_color"]["field_content"] = menstrual_color
            menstrual_quality = menstrual_history.get("menstrualQuality")
            if menstrual_quality:
                personal_dict["menstrual_quality"]["field_content"] = menstrual_quality
    else:
        # 男性或未知性别，所有月经相关字段设为 "无"
        menstrual_fields = ["menstrual_history", "menstrual_cycle", "menstrual_duration",
                            "last_menstrual_period", "menstrual_flow", "menstrual_color", "menstrual_quality"]
        for field in menstrual_fields:
            personal_dict[field]["field_content"] = "无"

    # 婚育史
    if marriage_child_info and isinstance(marriage_child_info, dict):
        personal_dict["marital_reproductive_history"]["field_content"] = "有"
        marriage_status = marriage_child_info.get("marriageStatus")
        if marriage_status:
            personal_dict["marital_status"]["field_content"] = marriage_status
        # 判断是否有生育史
        has_childbirth = any([
            marriage_child_info.get("fullTermCount", 0) > 0,
            marriage_child_info.get("prematureCount", 0) > 0,
            marriage_child_info.get("abortionCount", 0) > 0
        ])
        personal_dict["childbirth_status"]["field_content"] = "有" if has_childbirth else "无"
        full_term = marriage_child_info.get("fullTermCount")
        if full_term is not None:
            personal_dict["full_term_birth_count"]["field_content"] = full_term
        preterm = marriage_child_info.get("prematureCount")
        if preterm is not None:
            personal_dict["preterm_birth_count"]["field_content"] = preterm
        miscarriage = marriage_child_info.get("abortionCount")
        if miscarriage is not None:
            personal_dict["miscarriage_count"]["field_content"] = miscarriage
        living_children = marriage_child_info.get("livingChildrenCount")
        if living_children is not None:
            personal_dict["living_children_count"]["field_content"] = living_children
        children = marriage_child_info.get("childrenCount")
        if children is not None:
            personal_dict["children_count"]["field_content"] = children
    else:
        personal_dict["marital_reproductive_history"]["field_content"] = "无"
        # 相关字段保持为 None

    # 返回填充后的字段，保持字段顺序
    return {
        "condition_fields": condition_fields,  # 基本症状相关字段保持 None
        "history_fields": history_fields,
        "personal_fields": personal_fields,
    }

# 示例调用
if __name__ == "__main__":
    sample_data = '''
    {
      "patientIdentity": {
        "patientId": "PID123456",
        "idType": "01",
        "idNumber": "110101199001011234"
      },
      "latestMedicalRecord": {
        "basicInfo": {
          "gender": "女",
          "birthday": "1985-05-20",
          "aboBloodType": "A",
          "rhBloodType": "+"
        },
        "vitalSigns": {
          "systolicPressure": 120,
          "diastolicPressure": 80,
          "height": 165,
          "weight": 55
        },
        "marriageChildInfo": {
          "marriageStatus": "已婚",
          "fullTermCount": 1,
          "prematureCount": 0,
          "abortionCount": 0,
          "livingChildrenCount": 1,
          "childrenCount": 1
        },
        "pastHistory": {
          "personalHistory": "无特殊",
          "badHabits": "吸烟",
          "smoking": true,
          "smokingFrequency": "每天一包",
          "drinking": true,
          "drinkingFrequency": "偶尔",
          "lateNight": false,
          "dietaryStatus": "正常",
          "sleepStatus": "良好",
          "bowelMovement": "正常",
          "urineStatus": "正常",
          "menstrualHistory": {
            "menarcheAge": 13,
            "intervalDays": 28,
            "durationDays": 5,
            "isSterilization": false,
            "lastMenstrualDate": "2024-10-01",
            "menstrualFlow": "适中",
            "menstrualColor": "鲜红",
            "menstrualQuality": "规律"
          },
          "diseaseHistory": "高血压",
          "diseaseDiagnosisTime": "2010-05",
          "infectiousDiseaseHistory": {
            "diseaseName": "流感",
            "treatment": "是"
          },
          "allergyFoodName": "海鲜",
          "surgeryHistory": "阑尾炎手术史",
          "surgeryName": "阑尾切除术",
          "surgeryTime": "2005-08",
          "surgeryMedicalInstitution": "市中心医院",
          "familyHistory": {
            "relative": "父亲",
            "disease": "糖尿病"
          },
          "longTermMedicationHistory": {
            "medicationName": "降压药"
          }
        },
        "allergyHistory": "青霉素过敏",
        "childGrowthInfo": null
      },
      "revisitInfo": {
        "isRevisit": true,
        "lastRecord": {
          "chiefComplaint": "头痛3天",
          "presentIllness": "近3天持续性头痛",
          "conditionLocation": "头部",
          "conditionSeverity": "中度",
          "associatedSymptoms": "恶心",
          "menstrualHistory": {
            "menarcheAge": 13,
            "intervalDays": 28,
            "durationDays": 5,
            "isSterilization": false,
            "lastMenstrualDate": "2024-09-25",
            "menstrualFlow": "适中",
            "menstrualColor": "鲜红",
            "menstrualQuality": "规律"
          },
          "tcmFourExams": {
            "inspection": "面色苍白",
            "inquiry": "有胃脘隐痛史",
            "listeningAndSmelling": "口气稍重",
            "palpation": "脉沉细"
          },
          "physicalExam": "心肺听诊正常",
          "auxiliaryExam": "无异常",
          "diagnosis": {
            "tcmDiagnosisName": "头痛",
            "tcmDiagnosisCode": "TCM-001",
            "tcmSyndromeName": "肝阳上亢",
            "westernDiagnosisName": "神经性头痛",
            "westernDiagnosisCode": "G44.2"
          },
          "treatmentPrinciple": "平肝潜阳，活血通络",
          "treatmentAdvice": "注意休息，避免劳累",
          "prescription": {
            "prescriptionName": "平肝潜阳汤",
            "herbs": [
              "天麻",
              "钩藤",
              "栀子"
            ]
          }
        }
      }
    }
    '''
    result = main(sample_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
