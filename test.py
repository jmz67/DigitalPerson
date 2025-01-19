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

    # 1. 获取当前阶段对应的字段列表
    fields = stage_map.get(current_stage)
    if not fields:
        raise ValueError(f"未知的阶段：{current_stage}")

    # 2. 定义判断是否跳过该字段的函数
    def is_skip_field(user_answer: str) -> bool:
        """
        当用户回答包含 '无'、'没有' 或 '以上都没有' 时，视为需要跳过
        """ 
        negative_words = ["无", "没有", "以上都没有"]
        return any(neg_word in user_answer for neg_word in negative_words)

    # 3. 定义每个阶段需要跳过的字段映射表
    #    当某一字段回答为“无”或“没有”时，跳过其对应的字段（赋空字符串）
    skip_fields_map = {
        "症状": {
            "基本症状": ["症状持续时间", "症状部位", "症状严重程度", "伴随症状"],
            "有无就诊治疗过": ["就诊诊断"],
            "有无自行使用过药物或者采取过其他治疗措施": ["药物名称", "治疗措施名称"],
        },
        "既往史": {
            "有无慢性疾病": ["慢性疾病名称", "慢性病确诊时间"],
            "有无传染病史": ["传染病名称", "是否进行治疗"],
            "有无过敏史": ["过敏食物或药物名称"],  # 示例：根据实际字段自行调整
            "有无手术史": ["手术时间", "手术名称", "手术医疗机构"],
            "家属有无相关家族史": ["亲属关系", "家族史疾病名称"],
            "有无长期用药史": ["长期用药名称"],
        },
        "个人史": {
            "是否有不良生活习惯": [],
            "是否抽烟": [],  # 如果还有需要跳过的字段可以在此处加上
            "是否经常熬夜": [],
        },
    }

    # 获取需要跳过的字段列表
    skip_fields = skip_fields_map.get(current_stage, {}).get(current_field, [])

    # 4. 核心逻辑：遍历当前阶段字段列表，找到当前字段并进行处理
    for index, item in enumerate(fields):
        if item["field_name_cn"] == current_field:
            # 如果审核通过（答案“符合”）
            if approval == "符合":
                # 更新当前字段的内容
                item["field_content"] = answer

                # 如果用户回答需要跳过后续关联字段，则置空这些字段
                if is_skip_field(answer):
                    # 跳过 skip_fields 中指定的字段（赋空字符串）
                    for next_item in fields[index + 1:]:
                        if next_item["field_name_cn"] in skip_fields:
                            next_item["field_content"] = ""

                # 在当前阶段查找下一个尚未填写的字段
                for next_item in fields[index + 1:]:
                    # 如果该字段还是 None，说明还没填写，则跳转到这个字段
                    if next_item["field_content"] is None:
                        return {
                            "condition_fields": condition_fields,
                            "history_fields": history_fields,
                            "personal_fields": personal_fields,
                            "current_stage": current_stage,
                            "current_field": next_item["field_name_cn"]
                        }

                # 如果当前阶段所有字段均已填写或跳过，则切换到下一个阶段
                next_stage_index = stage_order.index(current_stage) + 1
                if next_stage_index < len(stage_order):
                    next_stage = stage_order[next_stage_index]
                    next_stage_fields = stage_map[next_stage]

                    # 查找下一个阶段里尚未填写的字段
                    for field_item in next_stage_fields:
                        if field_item["field_content"] is None:
                            return {
                                "condition_fields": condition_fields,
                                "history_fields": history_fields,
                                "personal_fields": personal_fields,
                                "current_stage": next_stage,
                                "current_field": field_item["field_name_cn"]
                            }

                    return {
                        "condition_fields": condition_fields,
                        "history_fields": history_fields,
                        "personal_fields": personal_fields,
                        "current_stage": None,
                        "current_field": None
                    }
                else:
                    # 已经是最后一个阶段，并且全部填完
                    return {
                        "condition_fields": condition_fields,
                        "history_fields": history_fields,
                        "personal_fields": personal_fields,
                        "current_stage": None,
                        "current_field": None
                    }

            else:
                # 如果答案不符合要求，则仍停留在当前字段
                return {
                    "condition_fields": condition_fields,
                    "history_fields": history_fields,
                    "personal_fields": personal_fields,
                    "current_stage": current_stage,
                    "current_field": current_field
                }

    # 如果循环结束还没找到当前字段（或者当前阶段所有字段都填写了），
    # 则尝试切换到下一个阶段。
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

    # 如果所有阶段均已填写完毕，则返回完成标识
    return {
        "condition_fields": condition_fields,
        "history_fields": history_fields,
        "personal_fields": personal_fields,
        "current_stage": None,
        "current_field": None
    }
