import time

import dash
from server import app, redis_pool
from dash import dcc, html
import feffery_antd_components as fac
import json
from dash.dependencies import ClientsideFunction, Input, Output, State
import random
from api.ABNReal.alarm_record import AlarmRecordApi
import plotly.express as px
from datetime import datetime
from dateutil import parser
import pandas as pd

REAL_INTERVAL = 4000  # 容器刷新时间间隔

# app.clientside_callback(
#     ClientsideFunction(namespace='clientside', function_name='render_chart'),
#     Output('ABN-real-module-chart', 'children'),
#     Input('ABN-temp-interval', 'n_intervals'), )

# 第一次加载首条数据
app.clientside_callback(
    ClientsideFunction(namespace='clientsideKjz', function_name='render_goChart_kjz'),
    Output('ABN-real-module-gojs-kjz', 'children', ),
    [
        Input('ABN-real-module-store-clicktable-kjz', 'data'),
        Input('ABN-real-module-store-clicktable-dataDesc-kjz', 'data')
    ]

)


@app.callback(
    Output('ABNReal-recent-record-card-kjz', 'children'),
    Input('ABN-real-module-store-clicktable-data-kjz', 'data'),
    prevent_initial_call=True,
)
def ABNReal_recent_record_card(data):
    if len(data) == 0:
        return "暂无近期报警记录"
    else:
        return [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                fac.AntdText("\U0001F538"),
                                style={
                                    'flex': '0 1',
                                    'marginRight': '16px',
                                },
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Span(
                                                f"报警时间：{item.get('ALARM_TIME')}，"
                                            ),
                                            html.Span(
                                                f"持续"
                                                + (
                                                    "{:.2f}".format(
                                                        (
                                                                datetime.strptime(item.get("UPDATE_TIME"),
                                                                                  "%Y-%m-%dT%H:%M:%S")
                                                                - datetime.strptime(item.get("ALARM_TIME"),
                                                                                    "%Y-%m-%dT%H:%M:%S")
                                                        ).total_seconds()
                                                    ) + "秒。"
                                                    if item.get("UPDATE_TIME") is not None and item.get(
                                                        "ALARM_TIME") is not None
                                                    else "未结束"
                                                )
                                            )
                                        ],
                                        key=str(item.get(
                                            'ID'
                                        )),
                                    ),
                                    html.Div(
                                        f"故障名称：{item.get('ANOMALY_NAME')} | 数据来源：实时遥测",
                                        style={
                                            'fontSize': '14px',
                                            # 'lineHeight': '22px',
                                        },
                                    ),
                                ],
                                style={
                                    'flex': '1 1 auto'
                                },
                            ),
                        ],
                        style={'display': 'flex'},
                    ),
                    fac.AntdDivider(
                        style={
                            'margin-bottom': '10px',
                            'margin-top': '15px'
                        }
                    ),
                ]
            )
            for item in data
        ]


# @app.callback(
#
#     Input('ABN-temp-interval', 'n_intervals'),
#     Input('ABN-real-module-store', 'data'),
#     prevent_initial_call=True,
# )
# def logout_confirm(data):
#     if data == None:
#         return ''
#     return f"报警总数{len(data)},"

def simple_format_and_sort(list1, list2, time_key="UPDATE_TIME"):
    readStatusYC = redis_pool.hgetall_by_pattern_str(pattern='anomaly:read_status:*')
    readStatusGC = redis_pool.hgetall_by_pattern_str(pattern='eng:read_status:*')
    finalStatus = readStatusYC | readStatusGC
    result = {json.loads(finalStatus[item])["MODEL_UUID"]: str(json.loads(finalStatus[item])["STATUS"]) for item in finalStatus}
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
            MODEL_UUID = data['MODEL_UUID']
            data["readStatus"] = result[MODEL_UUID]
            # 用于排序的时间对象
            sort_time = datetime.strptime(formatted_time, "%Y-%m-%d %H:%M:%S.%f")

            json_str = json.dumps(data, ensure_ascii=False)
            processed.append((json_str, sort_time))

        except (json.JSONDecodeError, ValueError) as e:
            print(f"处理失败: {e}")
            continue

    # 排序并返回
    sorted_items = sorted(processed, key=lambda x: x[1],reverse=True)
    return [item[0] for item in sorted_items]


@app.callback(
    [
        Output('ABN-real-module-store-kjz', 'data'),
        Output('statistic-info-text-kjz', 'htmlString'),
        Output('ABN-real-module-table-kjz', 'data'),
    ],
    Input('ABN-temp-interval-kjz', 'n_intervals'),
    State('ABNMode-Tabs-kjz', 'activeKey'),
    prevent_initial_call=True

)
def store_real_data(n_intervals, activeKey):
    # start_time = time.time()
    dataYCRedis = list(redis_pool.hgetall_by_pattern_str_sync(pattern='anomaly:alarm_info:*').values())
    dataEndRedis = list(redis_pool.hgetall_by_pattern_str_sync(pattern='eng:alarm_info:*').values())
    filter_condition = list(redis_pool.hgetall_by_pattern_str_sync(pattern="platform:anomaly:false_alarms:*").values())
    filter_condition_list = set()
    for filter_condition_item in filter_condition:
        # filter_condition_item_json = json.loads(filter_condition_item)
        filter_condition_list.add(filter_condition_item["key"])
    # print(f"redis数据拉取: {time.time() - start_time:.3f}s")
    # start_time = time.time()
    sorted_list = simple_format_and_sort(dataYCRedis, dataEndRedis)
    # print(f"表格数据加载: {time.time() - start_time:.3f}s")
    sorted_list = filter(
        lambda x: f'{json.loads(x)["ANOMALY_NO"]}@{json.loads(x)["ANOMALY_NAME"]}' not in filter_condition_list,
        sorted_list)
    dataToTable = []
    # start_time = time.time()
    for index, data in enumerate(sorted_list):
        data = json.loads(data)
        # print(data)
        dataToTable.append(
            {
                'uuid': data['MODEL_UUID'],
                'key': f'row-{index}',
                'dataIndex': index + 1,
                'ABNNo': data['ANOMALY_NO'],
                'ABNName': data['ANOMALY_NAME'],
                'payload': data['PAYLOAD_NAME'],
                'startTime': data['ALARM_TIME'],
                'updateTime': data['UPDATE_TIME'],
                'DATA_SOURCE': data['DATA_SOURCE'],
                'END_FLAG': "是" if data['END_FLAG'] else "否",
                'VARIABLES': data['VARIABLES'],
                'readStatusText': "未读" if 'readStatus' in data and data['readStatus'] == "0" else "已读",
                'ruleVersion': [{
                    'tag': f'{["稳定版本", "测试版本", "频发故障"][int(random.uniform(1, 1))]}',
                    'color': f'{["volcano", "blue", "geekblue"][int(random.uniform(1, 1))]}',
                }],
                'CSV_INFO': data['CSV_INFO'] if 'CSV_INFO' in data else [],
                'action': [
                    {
                        'content': '查看',
                        'type': 'primary',
                    },
                    # {
                    #     'content': '处置',
                    #     'type': 'primary',
                    # },
                    # {
                    #     'content': '静默',
                    #     'type': 'primary',
                    # },
                    {
                        'content': '误报',
                        'type': 'primary',
                    },
                    # {
                    #     'content': '已读',
                    #     'type': 'primary',
                    # }
                ]
            }
        )
    # print(f"表格数据组织: {time.time() - start_time:.3f}s")
    messages_s = redis_pool.get('anomaly:messages_s')
    messages_active = redis_pool.get('anomaly:messages_active')
    messages_received_total = redis_pool.get('anomaly:messages_received_total')
    return [dataToTable,
            f"<span>3天内报警总数:</span> <span style='color: purple;'>{len(dataToTable)}</span>, "
            f"<span>处理速率:</span> <span style='color: purple;'>{messages_s}包/s</span>, "
            f"<span>正在处理:</span> <span style='color: purple;'>{messages_active}包</span>, "
            f"<span>总接收:</span> <span style='color: purple;'>{messages_received_total}包</span>, ",
            dataToTable]


# @app.callback(
#     Output('ABN-real-module-table', 'data', allow_duplicate=True),
#     Input('ABN-real-module-store', 'data'),
#     prevent_initial_call=True,
# )
# def render_table(data):
#     return data


@app.callback(
    [
        Output('ABN-interval-parent-kjz', 'children'),
        Output('ABN-real-module-store-clicktable-kjz', 'data', allow_duplicate=True),
        Output('ABN-real-module-store-clicktable-dataDesc-kjz', 'data', allow_duplicate=True),
        Output('fullscreen-gojs-title', 'children', allow_duplicate=True)
    ],
    Input('ABNMode-Tabs-kjz', 'activeKey'),
    Input('url-kjz', 'pathname'),
    prevent_initial_call=True,
)
def initABNRealModule(activeKey, pathname):
    if activeKey in [None, '故障模式实时报警'] and pathname == '/ABNModule/ABNRealKjz':
        start_time = time.time()
        dataYCRedis = redis_pool.mget(key='anomaly:alarm_info:*')
        dataEndRedis = redis_pool.mget(key='eng:alarm_info:*')
        sorted_list = simple_format_and_sort(dataYCRedis, dataEndRedis)

        if len(sorted_list) == 0:
            return [dash.no_update, dash.no_update, {},f'判据描述信息：']
        json_data_redis = json.loads(sorted_list[0])
        ANOMALY_NO = json_data_redis.get("ANOMALY_NO")
        ANOMALY_NAME = json_data_redis.get("ANOMALY_NAME")
        DATA_SOURCE = json_data_redis.get("DATA_SOURCE")
        key = f'anomaly:global_status:{ANOMALY_NO}@{ANOMALY_NAME}' if DATA_SOURCE == "实时遥测" else f'eng:global_status:{ANOMALY_NO}@{ANOMALY_NAME}'
        desc_redis = redis_pool.hgetall(key=key)
        print(f"初始化拉取数据: {time.time() - start_time:.3f}s")
        return [dcc.Interval(id='ABN-temp-interval-kjz', interval=REAL_INTERVAL), json_data_redis,
                json.loads(desc_redis.get('description')) if desc_redis is not None else {},
                f'判据描述信息：{ANOMALY_NO}@{ANOMALY_NAME}']
    else:
        return [html.Div(), dash.no_update, {}, f'判据描述信息：']


# @app.callback(
#     Output('ABN-interval-parent', 'children'),
#     Input('ABNMode-Tabs', 'activeKey'),
#     Input('url', 'pathname'),
# )
@app.callback(
    [
        Output('ABN-real-module-store-clicktable-kjz', 'data', allow_duplicate=True),
        Output('ABN-real-module-store-clicktable-dataDesc-kjz', 'data', allow_duplicate=True),
        Output('fullscreen-gojs-title', 'children', allow_duplicate=True)
    ],
    [
        Input('ABN-real-module-table-kjz', 'nClicksCell'),
        Input('ABN-real-module-table-kjz', 'nDoubleClicksCell'),
    ],
    [
        State('ABN-real-module-table-kjz', 'recentlyCellClickRecord'),
    ],
    prevent_initial_call=True,
)
def click_table(nClicksCell, nDoubleClicksCell, click_data):
    ANOMALY_NO = click_data.get('ABNNo')
    ANOMALY_NAME = click_data.get('ABNName')
    DATA_SOURCE = click_data.get('DATA_SOURCE')
    key = f'anomaly:global_status:{ANOMALY_NO}@{ANOMALY_NAME}' if DATA_SOURCE == "实时遥测" else f'eng:global_status:{ANOMALY_NO}@{ANOMALY_NAME}'
    desc_redis = redis_pool.hgetall(key=key)
    return [click_data, json.loads(desc_redis.get('description')) if desc_redis is not None else {},
            f'判据描述信息：{ANOMALY_NO}@{ANOMALY_NAME}']


@app.callback(
    Output('ABN-real-module-store-clicktable-data-kjz', 'data'),
    Input('ABN-real-module-store-clicktable-kjz', 'data'),
)
def store_click_info(data):
    # print(data)  # 录完之后金太导出model文件，model文件直接放在项目里，把需要回显的数据用这个函数读取，存到store中

    # query_param = dict(begin_time='2025-1-09',end_time='2025-1-29',page_num=1,page_size=5,anomaly_no='TGMTYY0203-019',anomaly_name='在线维修实验柜主供电异常（确认）')
    # res_test = AlarmRecordApi.list_search_alarm_record(query_param)
    # print(res_test)

    res = AlarmRecordApi.list_recent_alarm_record(
        anomaly_info=f'{data["ABNNo"] if data.get("ABNNo") != None else data["ANOMALY_NO"]}@'
                     f'{data["ABNName"].replace("/", "&&") if data.get("ABNNo") != None else data["ANOMALY_NAME"].replace("/", "&&")}@'
                     f'5')
    if res == None or res["code"] != 200:
        return dash.no_update
    return res["data"]


def get_compatible_value(data, possible_keys, default="无数据"):
    """
    从数据中兼容不同大小写的键，获取对应值
    :param data: 源数据字典（selectData）
    :param possible_keys: 可能的键名列表（如 ["Name", "name"]）
    :param default: 所有键都不存在时的默认值
    :return: 匹配到的值或默认值
    """
    if not isinstance(data, dict):  # 确保data是字典（容错）
        return default
    for key in possible_keys:
        if key in data:
            return data[key] if data[key] is not None else default  # 空值也显示默认
    return default


@app.callback(
    output=(dict(
        modal_visible=Output('menu-modal-kjz', 'visible', allow_duplicate=True),
        modal_title=Output('menu-modal-kjz', 'title', allow_duplicate=True),
        modal_children=Output('menu-modal-kjz', 'children', allow_duplicate=True),
        modal_width=Output('menu-modal-kjz', 'width', allow_duplicate=True),
    )),
    inputs=(dict(
        n_Clicks=Input('ABN-real-module-warn-manager-kjz', 'nClicks'),
    )),
    state=(dict(
        data=State('ABN-real-module-table-kjz', 'data'),
    )),
    prevent_initial_call=True,
)
def show_modal(
        n_Clicks,
        data
):
    filter_condition = redis_pool.mget(f"platform:anomaly:false_alarms:*")
    filter_condition_list = []
    for index, filter_condition_item in enumerate(filter_condition, start=1):
        filter_condition_item_json = json.loads(filter_condition_item)
        ABNNo = filter_condition_item_json["key"].split("@")[0]
        ABNName = filter_condition_item_json["key"].split("@")[1]
        filter_condition_list.append({
            "ABNNo": ABNNo,
            "ABNName": ABNName,
            "dataIndex": index,
            'action': [
                {
                    'content': '删除',
                    'type': 'primary',
                }, ]
        })
    return dict(
        modal_visible=True,
        modal_title="误报管理",
        modal_children=[
            fac.AntdRow(
                [fac.AntdCol(
                    [fac.AntdTransfer(
                        id="ABN-warn-manager-transfer-kjz",
                        dataSource=[{'key': f'{i["ABNNo"]}@{i["ABNName"]}',
                                     'title': f'{i["ABNName"]}'} for i in data],
                        targetKeys=[],
                        showSearch=True,
                        height=500,
                    ),
                        fac.AntdButton(
                            "确认",
                            id="ABN-warn-manager-transfer-button-kjz",
                            style={"marginTop": 10, "float": "right"}
                        )
                    ],
                    span=12
                ),
                    fac.AntdCol(
                        fac.AntdTable(
                            id="ABN-real-module-table-warn-rule-kjz",
                            columns=[
                                {'title': '序号', 'dataIndex': 'dataIndex', 'width': '50px',
                                 'renderOptions': {'renderType': 'ellipsis'}, },
                                {'title': '故障编号', 'dataIndex': 'ABNNo', 'width': '150px',
                                 'renderOptions': {'renderType': 'ellipsis'}, },
                                {'title': '故障名称', 'dataIndex': 'ABNName', 'width': '200px',
                                 'renderOptions': {'renderType': 'ellipsis'}, },
                                {
                                    'title': '操作',
                                    'dataIndex': 'action',
                                    'renderOptions': {'renderType': 'button'},
                                },
                            ],
                            data=filter_condition_list,
                            maxHeight=500
                        ),
                        span=12
                    )],
                gutter=10
            )

        ],
        modal_width="70%",
    )


@app.callback(
    [
        Output('ABN-real-module-table-warn-rule-kjz', 'data', allow_duplicate=True),
        Output('ABN-real-module-table-kjz', 'data', allow_duplicate=True),
        Output('ABN-warn-manager-transfer-kjz', 'dataSource', allow_duplicate=True),
    ],
    Input('ABN-real-module-table-warn-rule-kjz', 'nClicksButton'),
    [
        State('ABN-real-module-table-warn-rule-kjz', 'recentlyButtonClickedRow'),
        # State('ABN-real-module-table-warn-rule', 'data'),
    ],
    prevent_initial_call=True
)
def delete_data(nClick, click_data):
    if click_data is None:
        return dash.no_update
    # warn_data = filter(lambda x:x["ABNNo"] != click_data["ABNNo"] and x["ABNName"] != click_data["ABNName"], warn_table_data)
    redis_pool.delete(f"platform:anomaly:false_alarms:{click_data['ABNNo']}@{click_data['ABNName']}")
    dataYCRedis = redis_pool.mget(key='anomaly:alarm_info:*')
    dataEndRedis = redis_pool.mget(key='eng:alarm_info:*')
    sorted_list = simple_format_and_sort(dataYCRedis, dataEndRedis)

    filter_condition = redis_pool.mget(f"platform:anomaly:false_alarms:*")
    filter_condition_list = []
    filter_condition_list_keys = []
    for index, filter_condition_item in enumerate(filter_condition, start=1):
        filter_condition_item_json = json.loads(filter_condition_item)
        ABNNo = filter_condition_item_json["key"].split("@")[0]
        ABNName = filter_condition_item_json["key"].split("@")[1]
        filter_condition_list_keys.append(filter_condition_item_json["key"])
        filter_condition_list.append({
            "ABNNo": ABNNo,
            "ABNName": ABNName,
            "dataIndex": index,
            'action': [
                {
                    'content': '删除',
                    'type': 'primary',
                }, ]
        })
    # filter_list = list(
    #     filter(lambda x: f'{x["ABNNo"]}@{x["ABNName"]}' not in filter_condition_list_keys, sorted_list))
    sorted_list = filter(
        lambda x: f'{json.loads(x)["ANOMALY_NO"]}@{json.loads(x)["ANOMALY_NAME"]}' not in filter_condition_list_keys,
        sorted_list)
    dataToTable = []
    for index, data in enumerate(sorted_list):
        data = json.loads(data)
        # print(data)
        dataToTable.append(
            {
                'uuid': data['MODEL_UUID'],
                'key': f'row-{index}',
                'dataIndex': index + 1,
                'ABNNo': data['ANOMALY_NO'],
                'ABNName': data['ANOMALY_NAME'],
                'payload': data['PAYLOAD_NAME'],
                'startTime': data['ALARM_TIME'],
                'updateTime': data['UPDATE_TIME'],
                'DATA_SOURCE': data['DATA_SOURCE'],
                'END_FLAG': "是" if data['END_FLAG'] else "否",
                'VARIABLES': data['VARIABLES'],
                'readStatus': "未读" if 'readStatus' in data and data['readStatus'] == "0" else "已读",
                'ruleVersion': [{
                    'tag': f'{["稳定版本", "测试版本", "频发故障"][int(random.uniform(1, 1))]}',
                    'color': f'{["volcano", "blue", "geekblue"][int(random.uniform(1, 1))]}',
                }],
                'CSV_INFO': data['CSV_INFO'] if 'CSV_INFO' in data else [],
                'action': [
                    {
                        'content': '查看',
                        'type': 'primary',
                    },
                    # {
                    #     'content': '处置',
                    #     'type': 'primary',
                    # },
                    # {
                    #     'content': '静默',
                    #     'type': 'primary',
                    # },
                    {
                        'content': '误报',
                        'type': 'primary',
                    },
                    # {
                    #     'content': '已读',
                    #     'type': 'primary',
                    # }
                ]
            }
        )
    return [filter_condition_list, dataToTable, [{'key': f'{i["ABNNo"]}@{i["ABNName"]}',
                                                  'title': f'{i["ABNName"]}'} for i in dataToTable]]


@app.callback(
    [
        Output('ABN-real-module-table-warn-rule-kjz', 'data', allow_duplicate=True),
        Output('ABN-warn-manager-transfer-kjz', 'targetKeys', allow_duplicate=True),
        Output('ABN-real-module-table-kjz', 'data', allow_duplicate=True),
        Output('ABN-warn-manager-transfer-kjz', 'dataSource', allow_duplicate=True),
    ],
    Input('ABN-warn-manager-transfer-button-kjz', 'nClicks'),
    [
        State('ABN-warn-manager-transfer-kjz', 'targetKeys'),
        State('ABN-real-module-table-kjz', 'data'),
    ],
    prevent_initial_call=True
)
def handle_transfer_change(nClicks, targetKeys, table_data):
    for targetKeysItem in targetKeys:
        redis_pool.set(f"platform:anomaly:false_alarms:{targetKeysItem}", {"key": targetKeysItem})
    filter_condition = redis_pool.mget(f"platform:anomaly:false_alarms:*")
    filter_condition_list = []
    filter_condition_list_keys = []
    for index, filter_condition_item in enumerate(filter_condition, start=1):
        filter_condition_item_json = json.loads(filter_condition_item)
        ABNNo = filter_condition_item_json["key"].split("@")[0]
        ABNName = filter_condition_item_json["key"].split("@")[1]
        filter_condition_list_keys.append(filter_condition_item_json["key"])
        filter_condition_list.append({
            "ABNNo": ABNNo,
            "ABNName": ABNName,
            "dataIndex": index,
            'action': [
                {
                    'content': '删除',
                    'type': 'primary',
                }, ]
        })
    filter_list = list(
        filter(lambda x: f'{x["ABNNo"]}@{x["ABNName"]}' not in filter_condition_list_keys, table_data))
    return [filter_condition_list, [], filter_list, [{'key': f'{i["ABNNo"]}@{i["ABNName"]}',
                                                      'title': f'{i["ABNName"]}'} for i in filter_list]]


@app.callback(
    output=(dict(
        modal_visible=Output('menu-modal-kjz', 'visible', allow_duplicate=True),
        modal_title=Output('menu-modal-kjz', 'title', allow_duplicate=True),
        modal_children=Output('menu-modal-kjz', 'children', allow_duplicate=True),
        modal_width=Output('menu-modal-kjz', 'width', allow_duplicate=True),
        render_footer=Output('menu-modal-kjz', 'renderFooter', allow_duplicate=True),
        graph_data=Output('ABN-Check-YC-Modal-store-kjz', 'data', allow_duplicate=True),
        table_data=Output('ABN-real-module-table-kjz', 'data', allow_duplicate=True),
    )),
    inputs=(dict(
        n_Clicks=Input('ABN-real-module-table-kjz', 'nClicksButton'),
    )),
    state=(dict(
        click_content=State('ABN-real-module-table-kjz', 'clickedContent'),
        click_row=State('ABN-real-module-table-kjz', 'recentlyButtonClickedRow'),
        active_key=State('ABNMode-Tabs-kjz', 'activeKey'),
        table_data=State('ABN-real-module-table-kjz', 'data'),
    )),
    prevent_initial_call=True,
)
def show_modal(
        n_Clicks,
        click_content,
        click_row,
        active_key,
        table_data
):
    if (active_key in [None, '故障模式实时报警'] and click_content == "查看"):

        ANOMALY_NO = click_row.get('ABNNo')
        ANOMALY_NAME = click_row.get('ABNName')
        DATA_SOURCE = click_row.get('DATA_SOURCE')
        MODEL_UUID = click_row.get('uuid')
        key = click_row.get("key")
        new_table_data = [table_item if table_item.get("key") != key else {**table_item, 'readStatus': "1"} for
                          table_item in table_data]
        if DATA_SOURCE == "实时遥测":
            redis_pool.set(f"anomaly:read_status:{MODEL_UUID}", {"MODEL_UUID": MODEL_UUID, "STATUS": "1"})
        else:
            redis_pool.set(f"eng:read_status:{MODEL_UUID}", {"MODEL_UUID": MODEL_UUID, "STATUS": "1"})

        key = f'anomaly:global_status:{ANOMALY_NO}@{ANOMALY_NAME}' if DATA_SOURCE == "实时遥测" else f'eng:global_status:{ANOMALY_NO}@{ANOMALY_NAME}'
        selectData = redis_pool.hgetall(key=key)
        selectData = json.loads(selectData.get('raw-json'))
        dataSet = {}
        time_template = "%Y-%m-%dT%H:%M:%S.%f" if DATA_SOURCE == "实时遥测" else "%Y-%m-%d %H:%M:%S.%f"
        for item in click_row['VARIABLES']:
            data_key = f'anomaly:anomaly_data:{item}' if DATA_SOURCE == "实时遥测" else f'eng:anomaly_data:{item}'
            data = redis_pool.lrange(data_key)
            for dataItem in data:
                dataItem[0] = int(datetime.strptime(dataItem[0].strip(), time_template).timestamp() * 1000)
                dataItem[1] = float(dataItem[1])
            dataSet[item] = data
        return dict(
            modal_visible=True,
            modal_title="查看判据",
            modal_children=[
                fac.AntdRow(
                    [
                        fac.AntdCol(
                            [
                                fac.AntdDivider(
                                    '基本信息', innerTextOrientation='left'
                                ),
                                fac.AntdCard(
                                    [
                                        fac.AntdCardGrid(f'载荷名称：{click_row["payload"]}', style={'width': "50%"}),
                                        fac.AntdCardGrid(f'报警名称：{click_row["ABNName"]}', style={'width': "50%"}),
                                        fac.AntdCardGrid(f'开始时间：{click_row["startTime"]}', style={'width': "50%"}),
                                        fac.AntdCardGrid(f'更新时间：{click_row["updateTime"]}', style={'width': "50%"}),
                                        fac.AntdCardGrid(html.A(f'数据来源：{",".join(click_row["CSV_INFO"])}'),
                                                         style={'width': "100%"}),
                                    ],
                                    # bordered=False,
                                    size='small',
                                    # bodyStyle={'padding': '0px 1px 0px 0px', 'border': 0},
                                    # headStyle={'display':'none'},
                                    styles={
                                        'header': {'display': 'none'},
                                        'body': {'padding': '0px 1px 0px 0px', 'border': 0}
                                    },
                                    style={'borderRadius': '8px 8px 0 0'},
                                ),
                                fac.AntdDivider(
                                    '遥测数据', innerTextOrientation='left'
                                ),
                                html.Div(
                                    id="ABN-Check-YC-Modal-Chart-Container-kjz",
                                    style={
                                        'width': '100%',
                                        "height": 400,
                                        "background": "#141414",
                                        "overflow": "hidden",
                                        "padding": 10,
                                        "box-sizing": "border-box"
                                        # 'maxHeight': '500px',
                                        # 'overflowY': 'auto',
                                    },
                                )
                            ],
                            span=14
                        ),
                        fac.AntdCol(
                            [
                                fac.AntdDivider(
                                    '故障信息', innerTextOrientation='left'
                                ),
                                html.Div(
                                    fac.AntdDescriptions(
                                        [
                                            # 故障名称：可能的键 "Name"（大驼峰）或 "name"（小驼峰）
                                            fac.AntdDescriptionItem(
                                                get_compatible_value(selectData, ["Name", "name"]),
                                                label='故障名称',
                                                span=1
                                            ),
                                            # 设备名称：可能的键 "Device" 或 "device"
                                            fac.AntdDescriptionItem(
                                                get_compatible_value(selectData, ["Device", "device"]),
                                                label='设备名称',
                                                span=1
                                            ),
                                            # 舱段：可能的键 "segment"（小驼峰）或 "Segment"（大驼峰）
                                            fac.AntdDescriptionItem(
                                                get_compatible_value(selectData, ["segment", "Segment"]),
                                                label='舱段',
                                                span=1
                                            ),
                                            # 故障等级：可能的键 "FaultClassification" 或 "faultClassification"
                                            fac.AntdDescriptionItem(
                                                get_compatible_value(selectData,
                                                                     ["FaultClassification", "faultClassification"]),
                                                label='故障等级',
                                                span=1
                                            ),
                                            # 责任系统：可能的键 "ResponsibilitySystem" 或 "responsibilitySystem"
                                            fac.AntdDescriptionItem(
                                                get_compatible_value(selectData,
                                                                     ["ResponsibilitySystem", "responsibilitySystem"]),
                                                label='责任系统',
                                                span=1
                                            ),
                                            # 影响域：可能的键 "Risk" 或 "risk"
                                            fac.AntdDescriptionItem(
                                                get_compatible_value(selectData, ["Risk", "risk"]),
                                                label='影响域',
                                                span=1
                                            ),
                                            # 故障描述：可能的键 "Description" 或 "description"
                                            fac.AntdDescriptionItem(
                                                get_compatible_value(selectData, ["Description", "description"]),
                                                label='故障描述',
                                                span=3
                                            ),
                                            # 发生阶段：可能的键 "happenTime"（小驼峰）或 "HappenTime"（大驼峰）
                                            fac.AntdDescriptionItem(
                                                get_compatible_value(selectData, ["happenTime", "HappenTime"]),
                                                label='发生阶段',
                                                span=1
                                            ),
                                            # 处置方式：可能的键 "DisposeWay" 或 "disposeWay"
                                            fac.AntdDescriptionItem(
                                                get_compatible_value(selectData, ["DisposeWay", "disposeWay"]),
                                                label='处置方式',
                                                span=2
                                            ),
                                            # 处置方式描述：可能的键 "dispose"（小驼峰）或 "Dispose"（大驼峰）
                                            fac.AntdDescriptionItem(
                                                get_compatible_value(selectData, ["dispose", "Dispose"]),
                                                label='处置方式描述',
                                                span=3
                                            ),
                                        ],
                                        layout='vertical',
                                        size="small",
                                        column=3,
                                        bordered=True,
                                        styles={
                                            'label': {'fontWeight': 'bold'}
                                        }
                                        # title='故障信息',
                                        #         labelStyle={'fontWeight': 'bold'},
                                        # bordered=True,
                                    ),
                                )
                            ],
                            span=10
                        ),
                    ],
                    gutter=10,
                )

            ],
            modal_width="70%",
            render_footer=False,
            graph_data=dataSet,
            table_data=new_table_data
        )
    elif active_key in [None, '故障模式实时报警'] and click_content == "误报":
        return dict(
            modal_visible=True,
            modal_title="误报操作",
            modal_children=[html.Div("是否设置为误报")],
            modal_width="30%",
            render_footer=True,
            graph_data={},
            table_data=table_data
        )


@app.callback(
    [Output('ABN-real-module-table-kjz', 'data', allow_duplicate=True),
     Output('menu-modal-kjz', 'visible', allow_duplicate=True),
     ],
    Input('menu-modal-kjz', 'okCounts'),
    [State('menu-modal-kjz', 'title'),
     State('ABN-real-module-table-kjz', 'recentlyButtonClickedRow'),
     State('ABN-real-module-table-kjz', 'data'),
     # State('ABN-warn-manager-transfer', 'targetKeys')
     ],
    prevent_initial_call=True,
)
def modal_confirm_loading_reset(okCounts, title, click_row, table_data):
    if title == "误报操作":
        key = f'{click_row["ABNNo"]}@{click_row["ABNName"]}'
        redis_pool.set(f"platform:anomaly:false_alarms:{key}", {"key": key})
        filter_list = list(
            filter(lambda x: f'{x["ABNNo"]}@{x["ABNName"]}' != key, table_data))
        return [filter_list, False]

    if title == "误报管理":
        print("a")
        # for targetKeysItem in targetKeys:
        #     redis_pool.set(f"platform:anomaly:false_alarms:{targetKeysItem}", {"key": targetKeysItem})
        # filter_list = list(
        #     filter(lambda x: f'{x["ABNNo"]}@{x["ABNName"]}' not in targetKeys, table_data))
        # return [filter_list, False]
    return dash.no_update


app.clientside_callback(
    ClientsideFunction(namespace='clientsideKjz', function_name='render_modal_chart_kjz'),
    Output('ABN-real-module-store-no-output-kjz', 'data', allow_duplicate=True),
    Input('ABN-Check-YC-Modal-store-kjz', 'data'),
    prevent_initial_call=True,
)


@app.callback(
    [Output('fullscreen-gojs-kjz', 'isFullscreen')],
    Input('fullscreen-gojs-button-kjz', 'nClicks'),
    State('fullscreen-gojs-kjz', 'isFullscreen'),
    prevent_initial_call=True
)
def gojs_fullscreen(nClicks, isFullscreen):
    return [not isFullscreen]
