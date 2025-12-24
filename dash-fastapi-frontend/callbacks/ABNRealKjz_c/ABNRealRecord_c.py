import time

from server import app, redis_pool
from dash.dependencies import ClientsideFunction, Input, Output, State
import json
from dash import dcc, html
from datetime import datetime
import dash

RECORD_INTERVAL = 4000  # 容器刷新时间间隔


def simple_format_and_sort(list1, list2, time_key="UPDATE_TIME"):
    """简洁的格式化和排序"""

    def format_time(time_str):
        """格式化时间为统一格式"""
        # 首先去除首尾空格！！！
        time_str = time_str.strip()

        # 替换T为空格
        time_str = time_str.replace('T', ' ')
        # 确保有微秒
        if '.' not in time_str:
            time_str = time_str + '.000000'
        return time_str

    # 处理每个项目
    processed = []
    for item in list1 + list2:
        try:
            # 如果是字典，直接使用；如果是字符串，解析JSON
            if isinstance(item, dict):
                data = item
            else:
                data = json.loads(item)

            original_time = data.get(time_key, "")
            formatted_time = format_time(original_time)

            # 更新时间为格式化后的版本
            data[time_key] = formatted_time

            # 用于排序的时间对象
            sort_time = datetime.strptime(formatted_time, "%Y-%m-%d %H:%M:%S.%f")

            json_str = json.dumps(data, ensure_ascii=False)
            processed.append((json_str, sort_time))

        except (json.JSONDecodeError, ValueError) as e:
            print(f"处理失败: {e}")
            continue

    # 排序并返回
    sorted_items = sorted(processed, key=lambda x: x[1])
    return [item[0] for item in sorted_items]

@app.callback(
    [
        Output('ABNReal-RealRecord-store-kjz', 'data'),
        # Output('ABNReal-RealRecord-click-store-kjz', 'data', allow_duplicate=True),
    ],
    Input('temp-record-interval-kjz', 'n_intervals'),
    [
        State('ABNMode-Tabs-kjz', 'activeKey'),
        State('ABNReal-RealRecord-click-store-kjz', 'data'),
    ],
    prevent_initial_call=True
)
def store_monitoring_data(n_intervals, activeKey, data):
    # 1. 数据获取与合并（不变）
    if activeKey != '故障模式全局监控':
        return dash.no_update
    # dataTable = []
    all_monitoring_data = redis_pool.hgetall_by_pattern(pattern='anomaly:global_status:*')
    all_eng_data = redis_pool.hgetall_by_pattern(pattern='eng:global_status:*')
    final_data = all_monitoring_data | all_eng_data

    # 2. 合并后先过滤有效数据（不变）
    valid_final_data = []
    for monitor_info_parent in final_data.values():
        if monitor_info_parent is not None and monitor_info_parent.get("real-time") is not None:
            valid_final_data.append(monitor_info_parent)

    # 3. 排序（核心修改：处理时间字符串的 T 和开头空格）
    sorted_final_data = sorted(
        valid_final_data,
        key=lambda item: (
            # 第一排序键：None 对应 0（排前），有时间对应 1（排后）
            0 if json.loads(item["real-time"])["UPDATE_TIME"] is None else 1,
            # 第二排序键：预处理时间字符串后解析（去空格 + 替换 T）
            datetime.fromisoformat(
                # 步骤1：获取原始 UPDATE_TIME
                json.loads(item["real-time"])["UPDATE_TIME"]
                # 步骤2：去除首尾空格（处理开头/结尾空格）
                .strip()
                # 步骤3：将 T 替换为空格（适配 ISO 格式的两种分隔符）
                .replace("T", " ")
            ) if json.loads(item["real-time"])["UPDATE_TIME"] is not None else None
        ),
        reverse=True  # 降序（新时间在前）
    )

    # 4. 排序后解析字段（不变）
    dataTable = []
    for idx, monitor_info_parent in enumerate(sorted_final_data):
        monitor_info = json.loads(monitor_info_parent["real-time"])
        CURR_STATUS_TYPE = {
            'tag': '参数' if monitor_info['CURR_STATUS_TYPE'] == 'parameter' else '指令',
            'color': 'cyan' if monitor_info['CURR_STATUS_TYPE'] == 'parameter' else 'orange'
        }

        if monitor_info['ALARM_STATE'] in ['滑动窗口检测', '固定窗口检测']:
            alarm_status = 'processing'
        elif monitor_info['ALARM_STATE'] == '等待指令执行':
            alarm_status = 'warning'
        elif monitor_info['ALARM_STATE'] == '报警状态':
            alarm_status = 'error'
        ALARM_STATE = {
            'status': alarm_status,
            'text': monitor_info['ALARM_STATE']
        }

        if monitor_info['UPDATE_TIME'] is not None:
            UPDATE_TIME = monitor_info['UPDATE_TIME'].strip() if "T" not in monitor_info['UPDATE_TIME'] else \
                monitor_info['UPDATE_TIME'].replace("T", " ")
        else:
            UPDATE_TIME = None

        dataTable.append(
            {
                'key': f'row-{idx}',
                'dataIndex': idx,
                "MODEL_UUID": monitor_info['MODEL_UUID'],
                "CREATE_TIME": monitor_info['CREATE_TIME'],
                "ANOMALY_NO": monitor_info['ANOMALY_NO'],
                "ANOMALY_NAME": monitor_info['ANOMALY_NAME'],
                "PAYLOAD_NAME": monitor_info['PAYLOAD_NAME'],
                "UPDATE_TIME": UPDATE_TIME,
                "DATA_SOURCE": monitor_info['DATA_SOURCE'],
                "ALARM_STATE": ALARM_STATE,
                "CURR_STATUS_TYPE": CURR_STATUS_TYPE,
                "CURR_STATUS_WINDOW": monitor_info['CURR_STATUS_WINDOW'],
                "CURR_STATUS_INDEX": monitor_info['CURR_STATUS_INDEX'],
                "PROCESSOR_INFO": str(monitor_info['PROCESSOR_INFO']),
                "STATUS_INFO": str(monitor_info['STATUS_INFO']),
            }
        )
    # print(f"表格构建耗时: {time.time() - sort_start:.3f}s")
    # 5. 返回结果（不变）
    if sorted_final_data:
        # latest_data = [json.loads(sorted_final_data[0]["real-time"])] if len(data) == 0 else data
        return [dataTable]
    else:
        return [dataTable]


@app.callback(
    Output('ABNReal-RealRecord-table-kjz', 'data', allow_duplicate=True),
    Input('ABNReal-RealRecord-store-kjz', 'data'),
    prevent_initial_call=True

)
def show_monitoring_data(data):
    return data


@app.callback(
    [
        Output('temp-record-interval-kjz-div', 'children')
    ],
    Input('ABNMode-Tabs-kjz', 'activeKey'),
    prevent_initial_call=True
)
def initial_load(activeKey):
    if activeKey == '故障模式全局监控':
        return [dcc.Interval(id='temp-record-interval-kjz', interval=RECORD_INTERVAL),]
    else:
        return [dash.no_update]


@app.callback(
    [
        # Output('test_ouput-kjz', 'children'),
        Output('ABNReal-RealRecord-click-store-kjz', 'data', allow_duplicate=True),
        Output('ABN_real_record_divider-kjz', 'children'),
        Output('ABN_real_record_gojs-kjz', 'children', allow_duplicate=True),
    ],
    [
        Input('ABNReal-RealRecord-table-kjz', 'nClicksCell'),
        Input('ABNReal-RealRecord-table-kjz', 'nDoubleClicksCell'),
    ],
    [
        State('ABNReal-RealRecord-table-kjz', 'recentlyCellClickRecord'),
    ],
    prevent_initial_call=True,
)
def get_selected_record_info(nClicksCell, nDoubleClicksCell, recentlyCellClickRecord):
    anomaly_no = recentlyCellClickRecord.get('ANOMALY_NO')
    anomaly_name = recentlyCellClickRecord.get('ANOMALY_NAME')
    DATA_SOURCE = recentlyCellClickRecord.get('DATA_SOURCE')
    key = f'anomaly:global_status:{anomaly_no}@{anomaly_name}' if DATA_SOURCE == "实时遥测" else f'eng:global_status:{anomaly_no}@{anomaly_name}'
    record_info = redis_pool.hgetall(key=key)

    if record_info.get("real-time") is not None:
        return [
            # str(json.loads(record_info.get("real-time"))['PROCESSOR_INFO']),
            [json.loads(record_info.get("real-time"))], f'判读流程监控：{anomaly_no}@{anomaly_name}', None]
    else:
        return dash.no_update


# gojs渲染
app.clientside_callback(
    ClientsideFunction(namespace='clientsideKjz', function_name='render_goChart_ABN_real_record_kjz'),
    Output('ABN_real_record_gojs-kjz', 'children', ),
    Input('ABNMode-Tabs-kjz', 'activeKey'),
    Input('ABNReal-RealRecord-click-store-kjz', 'data'),
)
