def main(
    condition_fields: list,
    history_fields: list,
    personal_fields: list,
    current_stage: str,
    current_field: str,
    approval: str,
    answer: str
):
    """
    更新字段内容并切换到下一个未填写字段或阶段。
    """
    # 定义阶段及其顺序
    stage_order = ["症状", "既往史", "个人史"]
    stage_map = {
        "症状": condition_fields,
        "既往史": history_fields,
        "个人史": personal_fields
    }

    # 获取当前阶段对应的字段列表
    fields = stage_map.get(current_stage)

    if not fields:
        raise ValueError(f"未知的阶段：{current_stage}")

    # 判断是否需要跳过的字段，根据“无”、“没有”来判断
    def is_skip_field(answer):
        return any(neg_word in answer for neg_word in ["无", "没有", "以上都没有"])

    # 根据字段的回答来跳过的字段，字典存储跳过的字段
    skip_fields_map = {
        "个人史": {
            "是否有不良生活习惯": ["是否抽烟", "是否喝酒", "是否经常熬夜", "饮食与口味状况", "睡眠状况"],
            "是否抽烟": ["抽烟频率"],
            "是否喝酒": ["喝酒频率"],
            "是否经常熬夜": ["饮食与口味状况", "睡眠状况"],
        },
        "既往史": {
            "有无慢性疾病": ["慢性疾病名称", "确诊时间"],
            "有无传染病史": ["疾病名称", "是否进行治疗"],
            "有无过敏史": ["过敏食物名称", "药物名称"],
            "有无手术史": ["手术时间", "手术名称", "手术医疗机构"],
            "家属有无相关家族史": ["亲属关系", "疾病名称"],
            "有无长期用药史": ["长期用药名称"],
        },
        "症状": {
            "基本症状": ["症状持续时间", "症状部位", "症状严重程度", "伴随症状"],
            "有无就诊治疗过": ["就诊诊断"],
            "有无自行使用过药物或者采取过其他治疗措施": ["药物名称", "治疗措施名称"],
        }
    }

    # 获取当前字段对应的跳过字段列表
    skip_fields = skip_fields_map.get(current_stage, {}).get(current_field, [])
    skip_next_fields = False  # 用于标记是否跳过后续字段

    # 遍历当前阶段的字段列表
    for index, item in enumerate(fields):
        if item["field_name_cn"] == current_field:  # 找到当前字段
            if approval == "符合":
                # 更新字段内容
                item["field_content"] = answer  

                # 如果当前字段是 “有无” 类型且回答为 “无” 或 “没有”，跳过后续相关字段
                if is_skip_field(answer):
                    skip_next_fields = True

                # 查找当前阶段下一个未填写的字段
                for next_item in fields[index + 1:]:
                    if skip_next_fields and next_item["field_name_cn"] in skip_fields:
                        # 跳过相关字段并赋值为空字符串
                        next_item["field_content"] = ""
                        continue
                    if next_item["field_content"] is None:
                        return {
                            "condition_fields": condition_fields,
                            "history_fields": history_fields,
                            "personal_fields": personal_fields,
                            "current_stage": current_stage,
                            "current_field": next_item["field_name_cn"]
                        }

                # 如果当前阶段所有字段已填写完毕，切换到下一个阶段
                next_stage_index = stage_order.index(current_stage) + 1
                if next_stage_index < len(stage_order):
                    next_stage = stage_order[next_stage_index]
                    next_fields = stage_map[next_stage]
                    for next_item in next_fields:
                        if next_item["field_content"] is None:
                            return {
                                "condition_fields": condition_fields,
                                "history_fields": history_fields,
                                "personal_fields": personal_fields,
                                "current_stage": next_stage,
                                "current_field": next_item["field_name_cn"]
                            }

                # 如果所有阶段都已完成
                return {
                    "condition_fields": condition_fields,
                    "history_fields": history_fields,
                    "personal_fields": personal_fields,
                    "current_stage": None,
                    "current_field": None
                }
            else:
                # 如果答案不符合要求，保持在当前字段
                return {
                    "condition_fields": condition_fields,
                    "history_fields": history_fields,
                    "personal_fields": personal_fields,
                    "current_stage": current_stage,
                    "current_field": current_field
                }

    # 如果当前阶段没有找到对应字段或已完成所有字段
    next_stage_index = stage_order.index(current_stage) + 1
    if next_stage_index < len(stage_order):
        next_stage = stage_order[next_stage_index]
        next_fields = stage_map[next_stage]
        for next_item in next_fields:
            if next_item["field_content"] is None:
                return {
                    "condition_fields": condition_fields,
                    "history_fields": history_fields,
                    "personal_fields": personal_fields,
                    "current_stage": next_stage,
                    "current_field": next_item["field_name_cn"]
                }

    # 如果所有阶段都已完成
    return {
        "condition_fields": condition_fields,
        "history_fields": history_fields,
        "personal_fields": personal_fields,
        "current_stage": None,
        "current_field": "finished"
    }
