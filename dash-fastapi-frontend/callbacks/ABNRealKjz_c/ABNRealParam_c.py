import json
from datetime import datetime
from itertools import islice

import feffery_antd_components as fac
import dash
import numpy as np
from dash import dcc, html
from dash.dependencies import ClientsideFunction, Input, Output, State
import plotly.graph_objects as go
from server import app, redis_pool
from api.ABNReal.alarm_record import AlarmRecordApi
from flask import session
from utils.cache_util import CacheManager
import dash_echarts
import re

REAL_INTERVAL = 4000

option = {
    "backgroundColor": "#121212",
    "color": ["rgba(255,255,255,0.85)"],
    "textStyle": {
        "color": "rgba(255,255,255,0.85)"
    },
    "title": {"text": "参数曲线图", "textStyle": {
        "color": "rgba(255,255,255,0.85)"
    }},
    "tooltip": {"trigger": "axis"},
    "toolbox": {
        "show": True,
        "right": "10%",
        "itemSize": 24,
        "iconStyle": {
            "fontSize": 24
        },
        "feature": {
            "mark": {"show": True},
            "dataView": {"show": True, "readOnly": False,
                         "iconStyle": {"color": "rgba(255,255,255,0.85)", "fontSize": 24, }},
            # "magicType": {"show": True, "type": ['line', 'bar']},
            # "restore": {"show": True},
            # "saveAsImage": {"show": True}
        }
    },
    "legend": {"data": [], "textStyle": {
        "color": "rgba(255,255,255,0.85)"
    }},
    "xAxis": {
        "type": "category",
        "data": []
    },
    "yAxis": {"type": "value"},
    "series": []
}

chart_option = {
    "tooltip": {"formatter": "{a} <br/>{b}: {c}%"},
    "series": [
        {
            "name": "CPU使用率",
            "type": "gauge",
            "min": 0,
            "max": 100,
            "splitNumber": 10,
            "axisLine": {
                "lineStyle": {
                    "width": 10,
                    "color": [[0.3, "#67e0e3"], [0.7, "#37a2da"], [1, "#fd666d"]]
                }
            },
            "pointer": {"width": 5},
            "detail": {"formatter": "{value}%"},
            "data": [{"value": 1, "name": "CPU"}]
        }
    ]
}
ALARM_STATE = {
    '滑动窗口检测': 'processing',
    '固定窗口检测': 'processing',
    '等待指令执行': 'warning',
    '报警状态': 'error'
}


@app.callback(
    [
        Output("ABN-key-param-interval-card-kjz", 'children', allow_duplicate=True),
        Output("alarm-chart-row-2-child", 'option', allow_duplicate=True),
        Output("alarm-chart-row-3-child", 'items', allow_duplicate=True),
        Output("alarm-chart-row-3-child", "classNames")
    ],
    [
        Input('abn-real-param-alarm-table-kjz', 'nClicksCell'),
        Input('abn-real-param-alarm-table-kjz', 'nDoubleClicksCell'),
    ],
    [
        State('abn-real-param-alarm-table-kjz', 'recentlyCellClickRecord'),
    ],
    prevent_initial_call=True,
)
def toggle_flip(nClicksCell, nDoubleClicksCell, recentlyCellClickRecord):
    if not recentlyCellClickRecord:
        return dash.no_update

    interval = dcc.Interval(id='ABN-key-param-interval-card-kjz', interval=REAL_INTERVAL) if not \
        recentlyCellClickRecord['END_FLAG'] else dash.no_update
    data = AlarmRecordApi.get_param_data_of_paramId({"para_codes": ",".join(recentlyCellClickRecord['VARIABLES']), "fault_type":"parameter"}) if not \
        recentlyCellClickRecord['END_FLAG'] else AlarmRecordApi.search_alarm_data(
        uuid=recentlyCellClickRecord['MODEL_UUID'],
        para=True  # 获取参数报警数据
    )
    value_data = data["data"] if not recentlyCellClickRecord['END_FLAG'] else data["data"][0]["DATA"][0]
    option["legend"] = {"data": list(value_data.keys())}
    x_axis_values = None
    option["series"] = []
    for key, points in value_data.items():
        points = [json.loads(p) for p in points]
        points.sort(key=lambda x: datetime.fromisoformat(x[0]))
        x_values = [datetime.fromisoformat(t).strftime("%Y-%m-%d %H:%M:%S") for t, v in points]
        y_values = [float(v) for t, v in points]

        if x_axis_values is None:
            x_axis_values = x_values

        option["series"].append({
            "name": key,
            "type": "line",
            "data": y_values,
            "symbol": "circle",
            "symbolSize": 4,
            "itemStyle": {
                "borderColor": '#0de7d5d9',
                "borderWidth": 2
            },
            "lineStyle": {
                "color": "#0de7d5d9",
                "width": 3
            }
        })

    option["xAxis"]["data"] = x_axis_values

    expaned_content = AlarmRecordApi.get_info_by_fault_nos({"fault_nos": recentlyCellClickRecord['ANOMALY_NO'],"fault_type":"parameter" })

    expaned_content_to_desc = {
        key: [
            {"label": "uuid", "children": fac.AntdTooltip(
                item.get("model_uuid"),
                title=f'{item.get("model_uuid")}',
                placement="top",
            )},
            {"label": "参数代号", "children": item.get("anomaly_no")},
            {"label": "参数名称", "children": item.get("anomaly_name")},
            {"label": "当前阶段判读模式", "children": "滑动检测" if item.get("anomaly_type") == "sliding" else "固定窗口"},
            {"label": "是否有指令条件", "children": "是" if item.get("have_command") else "否"},
            {"label": "是否有终止指令", "children": "是" if item.get("have_command_termination") else "否"},
            {"label": "是否有终止参数规则", "children": "是" if item.get("have_judgment_termination") else "否"},
            {
                "label": "逻辑表达式",
                "children": item.get('curr_state').get('processor_info')[0].get('expression') + ";$x:" + item.get('curr_state').get('processor_info')[0].get('variables')[0]

            }
        ]
        for key, item in expaned_content.get("data").items()
    }
    alarm_chart_row_2_child_option = option
    alarm_chart_row_3_child_items = expaned_content_to_desc.get(recentlyCellClickRecord['ANOMALY_NO'])
    return [interval, alarm_chart_row_2_child_option, alarm_chart_row_3_child_items, {
        "content": "",
    }]


@app.callback(
    [
        Output('alarm-chart-row-2-child', 'option', allow_duplicate=True),
    ],
    [
        Input('ABN-key-param-interval-card-kjz', 'n_intervals'),
        Input('ABNMode-Tabs-kjz', 'activeKey'),
    ],
    [
        State('abn-real-param-alarm-table-kjz', 'recentlyCellClickRecord'),
    ],
    prevent_initial_call=True,
)
def update_param_curve(n_intervals, activeKey, recentlyCellClickRecord):
    if activeKey not in [None, '关键参数异常检测'] or not recentlyCellClickRecord or recentlyCellClickRecord.get('END_FLAG'):
        return dash.no_update
    data = AlarmRecordApi.get_param_data_of_paramId({
        "para_codes": ",".join(recentlyCellClickRecord['VARIABLES']),
        'fault_type': 'parameter'
    })
    option["legend"] = {"data": list(data["data"].keys())}
    # print(recentlyCellClickRecord['VARIABLES'])
    x_axis_values = None
    option["series"] = []
    for key, points in data["data"].items():
        points = [json.loads(p) for p in points]
        points.sort(key=lambda x: datetime.fromisoformat(x[0]))
        x_values = [datetime.fromisoformat(t).strftime("%Y-%m-%d %H:%M:%S") for t, v in points]
        y_values = [float(v) for t, v in points]

        if x_axis_values is None:
            x_axis_values = x_values

        existing_series = next((s for s in option["series"] if s["name"] == key), None)

        if existing_series:
            existing_series["data"] = y_values
        else:
            option["series"].append({
                "name": key,
                "type": "line",
                "data": y_values,
                "symbol": "circle",
                "symbolSize": 4,
                "itemStyle": {
                    "borderColor": '#0de7d5d9',
                    "borderWidth": 2
                },
                "lineStyle": {
                    "color": "#0de7d5d9",
                    "width": 3
                }
            })

    option["xAxis"]["data"] = x_axis_values
    return [option]


@app.callback(
    [
        Output('abn-real-param-monitor-table-kjz', 'data'),
        Output('abn-real-param-alarm-table-kjz', 'data')
    ],
    [
        Input('abn-real-param-kjz-cabin', 'value'),
    ],
)
def toggle_flip(cabinChecked):
    AlarmRecordApi.set_param_cabin_kjz(
        {"cabin": cabinChecked, "username": CacheManager.get('user_info').get('user_name')
        if CacheManager.get('user_info')
        else None})
    return dash.no_update


def get_abn_real_data(cabins):
    user_info = CacheManager.get('user_info')
    username = user_info.get('user_name') if user_info else None
    cabins = AlarmRecordApi.get_param_cabin_kjz({"username": username}).get("data")
    global_data_raw = redis_pool.hgetall_by_pattern(pattern='parameter:global_status:*')
    global_data = [json.loads(item.get("real-time")) for item in list(global_data_raw.values()) if "real-time" in item]
    sorted_data = sorted(
        global_data,
        key=lambda x: x.get("PAYLOAD_NAME")
    )
    global_data_filter = [
        {
            **item,
            "dataIndex": idx + 1,
            "key": item.get('MODEL_UUID'),
            "ALARM_STATE": {
                "status": ALARM_STATE[item.get("ALARM_STATE")],
                "text": item.get("ALARM_STATE")
            },
        }
        for idx, item in enumerate(sorted_data)
        if item.get("SEGMENT") in cabins
    ]

    return global_data_filter


def get_abn_alarm_real_data(cabins, alarm_pagination):
    alarm_info_raw = redis_pool.mget(key='parameter:alarm_info:*')
    alarm_info = [json.loads(item) for item in alarm_info_raw if item]
    alarm_info_sorted = sorted(
        alarm_info,
        key=lambda x: datetime.fromisoformat(x["UPDATE_TIME"]),
        reverse=True
    )
    alarm_info_filter = [
        {
            **item,
            "Index": idx + 1,
            "END_FLAG_TAG": {"tag": "是" if item["END_FLAG"] else "否", "color": "orange" if item["END_FLAG"] else "red"}
        }
        for idx, item in enumerate(alarm_info_sorted)
        if item.get("SEGMENT") in cabins
    ]
    all_alarm_param_now_data_start_index = (alarm_pagination.get("current") - 1) * alarm_pagination.get("pageSize")
    all_alarm_param_now_data_end_index = all_alarm_param_now_data_start_index + alarm_pagination.get(
        "pageSize")
    all_alarm_param_now_data = list(
        islice(alarm_info_filter, all_alarm_param_now_data_start_index, all_alarm_param_now_data_end_index))
    alarm_counts = redis_pool.get(key='parameter:alarm_counts')  # 近期报警个数
    messages_active = redis_pool.get(key='parameter:messages_active')  # 待处理包数
    messages_received_total = redis_pool.get(key='parameter:messages_received_total')  # 总处理包数
    messages_s = redis_pool.get(key='parameter:messages_s')  # 处理速率(包/秒)
    model_counts = redis_pool.get(key='parameter:model_counts')  # 监测参数总数
    cpu_percent = redis_pool.get(key='parameter:cpu_percent')  # CPU占用率
    memory_percent = redis_pool.get(key='parameter:memory_percent')  # 内存占用率

    front_children = [
        {"label": "近期报警个数", "children": alarm_counts},
        {"label": "待处理包数", "children": messages_active},
        {"label": "总处理包数", "children": messages_received_total},
        {"label": "处理速率", "children": f'{messages_s}包/秒'},
        {"label": "监测参数总数", "children": model_counts},
        {"label": "CPU占用率", "children": cpu_percent},
        {"label": "内存占用率", "children": memory_percent}
    ]

    alarm_pagination_new = {
        **alarm_pagination,
        "total": len(alarm_info_filter)
    }
    return all_alarm_param_now_data, front_children, alarm_pagination_new


def get_cabin():
    user_info = CacheManager.get('user_info')
    username = user_info.get('user_name') if user_info else None
    cabins = AlarmRecordApi.get_param_cabin_kjz({"username": username}).get("data")
    return cabins


# 初始化回调
@app.callback(
    [
        Output('abn-real-param-kjz-cabin', 'value'),
        Output('abn-real-param-monitor-table-kjz', 'data', allow_duplicate=True),
        Output('abn-real-param-alarm-table-kjz', 'data', allow_duplicate=True),
        Output('ABN-key-param-interval-parent-kjz', 'children'),
        Output('abn-real-param-monitor-table-kjz', 'expandedRowKeyToContent', allow_duplicate=True),
        Output('alarm-chart-row-1-child', 'items', allow_duplicate=True),
        Output('abn-real-param-alarm-table-kjz', 'pagination', allow_duplicate=True),
        Output('alarm-chart-row-2-child', 'option', allow_duplicate=True),
        Output('alarm-chart-row-3-child', 'items', allow_duplicate=True),

    ],
    Input('ABNMode-Tabs-kjz', 'activeKey'),
    [
        State('abn-real-param-alarm-table-kjz', 'pagination'),
    ],
    prevent_initial_call=True,
)
def initABNRealModule(activeKey, alarm_pagination):
    if activeKey in [None, '关键参数异常检测']:
        cabins = get_cabin()
        all_param_now_data = get_abn_real_data(
            cabins)

        all_alarm_param_now_data, front_children, alarm_pagination_new = get_abn_alarm_real_data(
            cabins, alarm_pagination)
        alarm_chart_row_2_child_option = option
        alarm_chart_row_3_child_items = [
            {"label": "uuid", "children": "点击上方记录查看报警信息"},
            {"label": "参数代号", "children": "点击上方记录查看报警信息"},
            {"label": "参数名称", "children": "点击上方记录查看报警信息"},
            {"label": "当前阶段判读模式", "children": "点击上方记录查看报警信息"},
            {"label": "是否有指令条件	", "children": "点击上方记录查看报警信息"},
            {"label": "是否有终止指令	", "children": "点击上方记录查看报警信息"},
            {"label": "是否有终止参数规则	", "children": "点击上方记录查看报警信息"},
            {"label": "逻辑表达式	", "children": "点击上方记录查看报警信息"},
        ]
        global_data_filter_content = [
            {"key": item.get('MODEL_UUID'), "content": fac.AntdDescriptions(
                items=[],
                bordered=True,
            )}
            for idx, item in enumerate(all_param_now_data)
        ]
        return [
            cabins,
            all_param_now_data,
            all_alarm_param_now_data,
            dcc.Interval(id='ABN-key-param-interval-parent-kjz', interval=REAL_INTERVAL),
            global_data_filter_content,
            front_children,
            # pagination_new,
            alarm_pagination_new,
            alarm_chart_row_2_child_option,
            alarm_chart_row_3_child_items
        ]
    return dash.no_update


# @app.callback(
#     [
#         Output('all-data-pagination', 'data'),
#     ],
#     [
#         Input('abn-real-param-monitor-table-kjz', 'pagination'),
#     ],
#     [
#         State('all-data-pagination', 'data'),
#     ],
#     prevent_initial_call=True
# )
# def all_data_pagination_on_change(pagination, pagination_store):
#     if pagination.get("pageSize") == pagination_store.get("pageSize") and pagination.get(
#             "current") == pagination_store.get("current"):
#         return dash.no_update
#     else:
#         return [{"pageSize": pagination.get("pageSize"), "current": pagination.get("current")}]


@app.callback(
    [
        Output('alarm-data-pagination', 'data'),
    ],
    [
        Input('abn-real-param-alarm-table-kjz', 'pagination'),
    ],
    [
        State('alarm-data-pagination', 'data'),
    ],
    prevent_initial_call=True
)
def all_alarm_data_pagination_on_change(pagination, pagination_store):
    if pagination.get("pageSize") == pagination_store.get("pageSize") and pagination.get(
            "current") == pagination_store.get("current"):
        return dash.no_update
    else:
        return [{"pageSize": pagination.get("pageSize"), "current": pagination_store.get("current")}]


# 定时刷新回调
@app.callback(
    [
        Output('abn-real-param-monitor-table-kjz', 'data', allow_duplicate=True),
        Output('abn-real-param-alarm-table-kjz', 'data', allow_duplicate=True),
        Output('alarm-chart-row-1-child', 'items', allow_duplicate=True),
        Output('abn-real-param-alarm-table-kjz', 'pagination', allow_duplicate=True),
    ],
    [
        Input('ABN-key-param-interval-parent-kjz', 'n_intervals'),
    ],
    [
        State('ABNMode-Tabs-kjz', 'activeKey'),
        State('abn-real-param-alarm-table-kjz', 'pagination'),
        State('abn-real-param-kjz-cabin', 'value'),
    ],
    prevent_initial_call=True
)
def store_real_data(n_intervals, activeKey, alarm_pagination, cabins):
    if activeKey in [None, '关键参数异常检测']:
        all_param_now_data = get_abn_real_data(
            cabins)
        all_alarm_param_now_data, front_children, alarm_pagination_new = get_abn_alarm_real_data(
            cabins, alarm_pagination)
        return [all_param_now_data, all_alarm_param_now_data, front_children,
                alarm_pagination_new,
                ]
    return dash.no_update


@app.callback(
    [
        Output('abn-real-param-monitor-table-kjz', 'expandedRowKeyToContent', allow_duplicate=True),
    ],
    [
        Input('abn-real-param-monitor-table-kjz', "expandedRowKeys"),
    ],
    [
        State('abn-real-param-monitor-table-kjz', 'data'),
        State('abn-real-param-monitor-table-kjz', 'expandedRowKeyToContent')
    ],
    prevent_initial_call=True
)
def play_data_callback(keys_data, data_source, data_expanded):
    if len(keys_data) == 0:
        return dash.no_update
    fault_nos = [item.get("ANOMALY_NO") for item in data_source if item.get("key") in keys_data]
    expaned_content = AlarmRecordApi.get_info_by_fault_nos({"fault_nos": ",".join(fault_nos), 'fault_type': 'parameter'})
    expaned_content_to_desc = {
        item.get('model_uuid'): [
            {"label": "uuid", "children": item.get("model_uuid")},
            {"label": "参数代号", "children": item.get("anomaly_no")},
            {"label": "参数名称", "children": item.get("anomaly_name")},
            {"label": "当前阶段判读模式", "children": "滑动检测" if item.get("anomaly_type") == "sliding" else "固定窗口"},
            {"label": "是否有指令条件", "children": "是" if item.get("have_command") else "否"},
            {"label": "是否有终止指令", "children": "是" if item.get("have_command_termination") else "否"},
            {"label": "是否有终止参数规则", "children": "是" if item.get("have_judgment_termination") else "否"},
            {
                "label": "逻辑表达式",
                "children": item.get('curr_state').get('processor_info')[0].get('expression') + ";$x:" + item.get('curr_state').get('processor_info')[0].get('variables')[0]
            }
        ]
        for key, item in expaned_content.get("data").items()
    }
    expaned_content = [{**item, "content": fac.AntdDescriptions(
        items=expaned_content_to_desc.get(item.get('key')),
        bordered=True,
    )} if item.get('key') in expaned_content_to_desc else {**item} for item in data_expanded]
    return [expaned_content]
