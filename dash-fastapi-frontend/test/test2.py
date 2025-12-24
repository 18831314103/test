import json
from typing import Dict, List, Any, Optional


class ConditionType:
    beat = "beat"
    delta = "delta"
    increase = "increase"
    formula = "formula"
    increase_setstep = "increase_setstep"
    count = "count"
    value = "value"
    range = "range"
    semialert = "semialert"


def get_crite_desc_by_command_condition(condition: Dict[str, Any]) -> str:
    """
    生成指令条件的HTML描述
    """
    sb = []

    # 处理发送状态
    state = condition.get("state", "0")
    if state == "0":
        sb.append("         <span prefix='是否发送:'  stuffix='' class='InstructionIdent'>")
        sb.append("  发送")
    elif state == "2":
        sb.append("         <span prefix='是否发送:'  stuffix='' class='InstructionIdent'>")
        sb.append("  未发送")

    if state in ["0", "2"]:
        sb.append(" </span>")

    # 事件名称
    event_name = condition.get("eventName", "")
    sb.append(f"<span class='InstructionName'>{event_name}</span>")
    sb.append("\r\n")

    # 标识信息
    identification = condition.get("identification", "")
    data_type = condition.get("dataType", "")
    sub_system_id = condition.get("subSystemID", "")
    action_function_id = condition.get("actionFunctionID", "")

    sb.append("         <span prefix='  标识:'  stuffix='' class='InstructionIdent'>")
    sb.append(f"{identification} {data_type} {sub_system_id} {action_function_id} </span>")
    sb.append("\r\n")

    # 参数列表
    param_list = condition.get("ParamList", [])
    for param in param_list:
        para_code = param.get("ParaCode", "")
        sb.append(f"<span prefix='   参数:'  stuffix='' class='InstructionParaCode'>{para_code}</span>")

    sb.append("\r\n")
    return "".join(sb)


def format_expression(expression: str, param_list: List[Dict[str, Any]]) -> str:
    """
    格式化表达式，将运算符和参数替换为自然语言
    """
    if not expression:
        return ""

    # 替换运算符
    exp = expression.replace("==", "等于") \
        .replace("!=", "不等于") \
        .replace(">=", "大于等于") \
        .replace("<=", "小于等于") \
        .replace(">", "大于") \
        .replace("<", "小于") \
        .replace("&", "且") \
        .replace("|", "或") \
        .replace("||", "或") \
        .replace("&&", "且")

    # 替换参数
    for param in param_list:
        code = param.get("code", "")
        name = param.get("name", "")
        if code and name:
            exp = exp.replace(f"${code}", f'"{name}"')

    return exp


def get_condition_desc(condition: Dict[str, Any]) -> str:
    """
    生成单个条件的HTML描述
    """
    sb = []

    # 参数索引
    index = condition.get("index", "")
    sb.append(f"<span prefix=''  stuffix='.' class='ParamIndex'>{index}</span>")

    # 条件类型
    type_ = condition.get("type", "")
    sb.append(" <span prefix=''  stuffix='' class='ParamType'>")

    if type_ == ConditionType.beat:
        sb.append("心跳参数")
    elif type_ == ConditionType.delta:
        sb.append("变化值：")
    elif type_ == ConditionType.increase:
        sb.append("差值：")
    elif type_ == ConditionType.formula:
        sb.append("自定义参数：")
    elif type_ == ConditionType.increase_setstep:
        sb.append("相邻帧增量：")
    elif type_ == ConditionType.count:
        sb.append("满足条件【")
    elif type_ == ConditionType.value:
        sb.append("值：")
    elif type_ == ConditionType.range:
        sb.append("范围：")
    elif type_ == ConditionType.semialert:
        sb.append("参数异常：")
    else:
        sb.append("未知类型")

    sb.append("</span>")

    # 处理表达式
    expression = condition.get("expression", "")
    param_list = condition.get("paramList", [])

    # 格式化表达式
    formatted_exp = format_expression(expression, param_list)

    # 处理特殊情况
    if type_ == ConditionType.count:
        formatted_exp = formatted_exp.replace(";$times", "】的出现次数 ")

    sb.append(f"<span prefix=''  stuffix='' class='ParamValue'>{formatted_exp}</span>")

    # 判断区间
    duration = condition.get("duration", {})
    duration_value = duration.get("value", "0")
    sb.append(f"<span prefix='，判断区间'  stuffix='秒;' class='ParamDuration'>{duration_value}</span>")

    return "".join(sb)


def process_judgment(judgment: Dict[str, Any]) -> str:
    """
    处理JudgMent部分，生成参数描述
    """
    full = []

    # 逻辑关系
    condition_expression = judgment.get("conditionExpression", "")
    full.append(f"<span prefix='逻辑关系:'  stuffix='' class='logic'>{condition_expression}  区间判读</span>")

    # 处理每个条件
    condition_arr = judgment.get("condition", [])

    # 按index排序
    condition_arr.sort(key=lambda x: int(x.get("index", "0")))

    for condition in condition_arr:
        full.append("<span class='judgment'>")
        full.append(get_condition_desc(condition))
        full.append("</span>")

    return "".join(full)


def get_fault_criterion_desc(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    主函数：将故障判据JSON转换为HTML描述
    """
    result = {
        "instructions": [],
        "params": [],
        "dataTerminate": {
            "instruction_Ter": [],
            "params_Ter": []
        }
    }

    # 处理指令条件
    command = json_data.get("Command", {})
    command_conditions = command.get("condition", [])

    for cond in command_conditions:
        # 添加state字段（默认为0，表示已发送）
        cond_with_state = cond.copy()
        cond_with_state["state"] = cond_with_state.get("state", "0")
        instruction_desc = get_crite_desc_by_command_condition(cond_with_state)
        result["instructions"].append(instruction_desc)

    # 处理JudgMent
    judgment = json_data.get("JudgMent", {})
    if judgment:
        param_desc = process_judgment(judgment)
        result["params"].append({"param": param_desc})

    # 处理RuleJudgMent（作为终止条件）
    rule_judgment = json_data.get("RuleJudgMent", {})
    if rule_judgment:
        rule_desc = process_judgment(rule_judgment)
        result["dataTerminate"]["params_Ter"].append({"param": rule_desc})

    return result


def main():
    """
    示例用法
    """
    # 示例输入数据
    input_json = {
        "No": "TGWTYY4002-111-2",
        "Name": "PSDU2主功率模块加电指令未响应",
        "Payload": "元器件",
        "Device": "元器件",
        "Description": "PSDU2主功率模块电压遥测＜0.5V",
        "Risk": "试验单元在轨试验中断",
        "disposeWay": "",
        "FaultClassification": "III",
        "happenTime": "在轨运行",
        "ResponsibilitySystem": "空间应用系统、元器件装置分系统",
        "RelevantSystem": "/",
        "Measure": "",
        "expression": "1->2",
        "SafeRequire": "",
        "ImpactAnalysis": "",
        "Invalid": "",
        "SafeMode": "",
        "Test_And": "",
        "RelevantPlans": "",
        "announcement": "",
        "YJ_duice": "",
        "PT_duice": "",
        "PT_zbgz": "",
        "PT_czqt": "",
        "JudgMent": {
            "condition": [
                {
                    "index": "1",
                    "type": "increase",
                    "expression": "$x==1",
                    "level": "",
                    "Forntexpression": "1",
                    "fornttype": "increase",
                    "paramList": [
                        {
                            "code": "x",
                            "id": "DCEW7171/1",
                            "name": "二级1553B/F1553总线数据注入(控制指令)计数",
                            "type": "int"
                        }
                    ],
                    "delayTime": {
                        "value": "130",
                        "unit": "sec"
                    },
                    "duration": {
                        "value": "120",
                        "unit": "sec"
                    }
                }
            ],
            "conditionExpression": "1"
        },
        "RuleJudgMent": {
            "condition": [
                {
                    "index": "1",
                    "type": "value",
                    "expression": "$x==010b",
                    "level": "",
                    "Forntexpression": "010b",
                    "fornttype": "value",
                    "paramList": [
                        {
                            "code": "x",
                            "id": "DCEW7160/2",
                            "name": "遥测段PSDU编号标识",
                            "type": "int"
                        }
                    ],
                    "delayTime": {
                        "value": "0",
                        "unit": "sec"
                    },
                    "duration": {
                        "value": "120",
                        "unit": "sec"
                    }
                },
                {
                    "index": "2",
                    "type": "value",
                    "expression": "$x==0",
                    "level": "",
                    "Forntexpression": "0",
                    "fornttype": "value",
                    "paramList": [
                        {
                            "code": "x",
                            "id": "DCEW7161/3",
                            "name": "PSDU主功率模块DC/DC1实时加断电状态标志位",
                            "type": "int"
                        }
                    ],
                    "delayTime": {
                        "value": "0",
                        "unit": "sec"
                    },
                    "duration": {
                        "value": "120",
                        "unit": "sec"
                    }
                },
                {
                    "index": "3",
                    "type": "value",
                    "expression": "$x==0",
                    "level": "",
                    "Forntexpression": "0",
                    "fornttype": "value",
                    "paramList": [
                        {
                            "code": "x",
                            "id": "DCEW7161/4",
                            "name": "PSDU主功率模块DC/DC2实时加断电状态标志位",
                            "type": "int"
                        }
                    ],
                    "delayTime": {
                        "value": "0",
                        "unit": "sec"
                    },
                    "duration": {
                        "value": "120",
                        "unit": "sec"
                    }
                },
                {
                    "index": "4",
                    "type": "value",
                    "expression": "$x==0",
                    "level": "",
                    "Forntexpression": "0",
                    "fornttype": "value",
                    "paramList": [
                        {
                            "code": "x",
                            "id": "DCEW7161/9",
                            "name": "主功率模块DC/DC1 +28V/+12V实时输出电压过欠压标志位",
                            "type": "int"
                        }
                    ],
                    "delayTime": {
                        "value": "0",
                        "unit": "sec"
                    },
                    "duration": {
                        "value": "120",
                        "unit": "sec"
                    }
                },
                {
                    "index": "5",
                    "type": "value",
                    "expression": "$x==0",
                    "level": "",
                    "Forntexpression": "0",
                    "fornttype": "value",
                    "paramList": [
                        {
                            "code": "x",
                            "id": "DCEW7161/10",
                            "name": "主功率模块DC/DC2 +28V/+12V实时输出电压过欠压标志位",
                            "type": "int"
                        }
                    ],
                    "delayTime": {
                        "value": "0",
                        "unit": "sec"
                    },
                    "duration": {
                        "value": "120",
                        "unit": "sec"
                    }
                }
            ],
            "conditionExpression": "1&(2||3)&(4||5)"
        },
        "plantime": "130",
        "Command": {
            "condition": [
                {
                    "index": "1",
                    "eventName": "元器件模块加电指令",
                    "identification": "1D15H",
                    "dataType": "C1H",
                    "subSystemID": "11H",
                    "actionFunctionID": "11H",
                    "ParamList": [
                        {
                            "ParaName": "目标单元类型-PSDU主功率模块",
                            "ParaCode": "1AH",
                            "Paraorder": "0"
                        },
                        {
                            "ParaName": "参数2-null",
                            "ParaCode": "015A5A5A5A5A5AH",
                            "Paraorder": "1"
                        }
                    ]
                }
            ],
            "conditionExpression": "1"
        },
        "dispose": "1.对元器件试验装置进行处置\n（1）\t发送 \"PSDU2主功率模块加电\"指令，判断参数1~7，若正常则结束处置；\n（2）\t若异常，发送 \"PSDU2主功率模块断电\"指令，10s后发送\"PSDU2主功率模块加电\"指令，判断参数1~7，若正常则结束处置；\n（3）\t若异常，发送\"PSDU2主功率模块断电\"指令，10s后发送\"PSDU2通信控制模块断电\"指令，10s后发送\"TCWY150\"主份关机，指令，10s后发送\"TCWY149\"主份开机指令，10s后发送\"上注指令（文件）-CMCU应用软件装订参数\"指令，10s后发送\"平台子系统状态数据回读\"指令（5遍），10s后发送\"上注指令（文件）-CMCU应用软件局部函数01-程序包\"指令，10s后发送\"上注指令（文件）校验\"指令，10s后发送\"上注指令（文件）-CMCU应用软件局部函数01-指令包\"指令，10s后发送\"上注指令（文件）校验\"指令，10s后发送\"PSDU2通信控制模块加电\"指令，10s后发送\"PSDU2主功率模块加电\"指令，判断参数1~7，若正常则结束处置；\n（4）\t若异常，10s后发送\"PSDU2主功率模块断电\"指令，10s后发送\"PSDU2通信控制模块断电\"指令，10s后发送\"TCWY150\"主份关机指令，10s后发送\"TCWY151\"备份开机指令，10s后发送\"上注指令（文件）-CMCU应用软件装订参数\"指令，10s后发送\"平台子系统状态数据回读\"指令（5遍），10s后发送\"上注指令（文件）-CMCU应用软件局部函数01-程序包\"指令，10s后发送\"上注指令（文件）校验\"指令，10s后发送\"上注指令（文件）-CMCU应用软件局部函数01-指令包\"指令，10s后发送\"上注指令（文件）校验\"指令，10s后发送\"PSDU2通信控制模块加电\"指令，10s后发送\"PSDU2主功率模块加电\"指令，判断参数1~7，若正常则结束处置；\n（5）\t若异常，10s后发送\"PSDU2主功率模块断电\"指令，10s后发送\"PSDU2通信控制模块断电\"指令，等待地面会商后，确定后续处置对策。\n\n\n",
        "segment": "TGWT"
    }

    # 转换为描述
    result = get_fault_criterion_desc(input_json)

    # 生成最终输出
    output = {
        "msg": "操作成功",
        "code": 200,
        "data": result
    }

    # 打印结果
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()