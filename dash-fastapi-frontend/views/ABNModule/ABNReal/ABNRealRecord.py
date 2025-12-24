import feffery_antd_components as fac
from dash import dcc, html
from callbacks.ABNReal_c import ABNRealRecord_c

RECORD_INTERVAL = 4000 # 容器刷新时间间隔

def render_ABNRealRecord():
    return [
        html.Div(
            [
                dcc.Store(id='ABNReal-RealRecord-store',data=[]),
                dcc.Store(id='ABNReal-RealRecord-click-store', data=[]),
                html.Div(id='ABNReal-RealRecord-interval'),
                html.Div(id='temp-record-interval-div'),
				# dcc.Interval(id='temp-record-interval', interval=RECORD_INTERVAL, n_intervals=1,disabled=True),
                # dcc.Interval(id='ABNReal-RealRecord-interval', interval=2000, n_intervals=1),
                fac.AntdTable(
                    columns=[
                        # {'title': 'UUID', 'dataIndex': 'MODEL_UUID'},
                        {'title': '序号', 'dataIndex': 'dataIndex', 'width': '50px',
                         'renderOptions': {'renderType': 'ellipsis'}, },
                        {'title': '创建时间', 'dataIndex': 'CREATE_TIME','renderOptions': {'renderType': 'ellipsis'},},
                        {'title': '故障编号', 'dataIndex': 'ANOMALY_NO','renderOptions': {'renderType': 'ellipsis'}},
                        {'title': '故障名称', 'dataIndex': 'ANOMALY_NAME','renderOptions': {'renderType': 'ellipsis'}},
                        {'title': '载荷', 'dataIndex': 'PAYLOAD_NAME','renderOptions': {'renderType': 'ellipsis'}},
                        # {'title': '报警时间', 'dataIndex': 'ALARM_TIME'},
                        {'title': '更新时间', 'dataIndex': 'UPDATE_TIME','renderOptions': {'renderType': 'ellipsis'},},
                        {'title': '数据来源', 'dataIndex': 'DATA_SOURCE','renderOptions': {'renderType': 'ellipsis'}},
                        {'title': '判读状态', 'dataIndex': 'ALARM_STATE','renderOptions': {'renderType': 'status-badge'}},
                        {'title': '当前判读类型', 'dataIndex': 'CURR_STATUS_TYPE','renderOptions': {'renderType': 'tags'}, },
                        # {'title': '判读窗口类型', 'dataIndex': 'CURR_STATUS_WINDOW'},
                        {'title': '当前判读阶段', 'dataIndex': 'CURR_STATUS_INDEX','renderOptions': {'renderType': 'ellipsis'}},
                        # {'title': '阶段信息', 'dataIndex': 'PROCESSOR_INFO'},
                        # {'title': '判读结果', 'dataIndex': 'STATUS_INFO'},
                    ],
                    filterOptions={
                        'ANOMALY_NO': {'filterMode': 'keyword'},
                        'ANOMALY_NAME': {'filterMode': 'keyword'},
                        'PAYLOAD_NAME': {'filterSearch': True},
                        'DATA_SOURCE': {'filterSearch': True},
                        'ALARM_STATE':{},
                        'CURR_STATUS_TYPE':{},
                        'CURR_STATUS_INDEX':{}
                    },
                    sortOptions={
                        'sortDataIndexes': [
                            'CREATE_TIME',
                            'UPDATE_TIME'
                        ]
                    },
                    id='ABNReal-RealRecord-table',
                    scrollToFirstRowOnChange=False,
                    maxHeight="19.8rem",
                    pagination={'pageSize': 10, 'hideOnSinglePage': True},
                    #bordered=True,
                    enableCellClickListenColumns=['CREATE_TIME','ANOMALY_NO','ANOMALY_NAME','PAYLOAD_NAME',
                                                  'UPDATE_TIME','DATA_SOURCE','ALARM_STATE','CURR_STATUS_TYPE','CURR_STATUS_INDEX']
                ),
            ]
        ),
        fac.AntdDivider(
            "判读流程监控",
            size="small",
            id="ABN_real_record_divider"
        ),
        html.Div(
            html.Div(
                id="ABN_real_record_gojs",
                style={
                    'fontSize': 18,
                    # "boxShadow": "rgb(240, 241, 242) 0px 2px 14px",
                    'height': 300,
                    "lineHeight":"300px",
                    "textAlign":"center",
                    "background": "rgb(31 33 34)"
                },
            ),
            style={
                "paddingTop": 10,
                # "background": "#D9EDF6"
            }
        ),
        fac.AntdText(
            id='test_ouput'
        ),
    ]
