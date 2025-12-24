import feffery_antd_components as fac
from datetime import datetime
import random
from dash import dcc, html
from dash.dependencies import Input, Output, ClientsideFunction
from openpyxl.styles.builtins import styles
from datetime import datetime, timedelta
from callbacks.ABNRealKjz_c import ABNRealParam_c
import dash_echarts

today = datetime.now()
seven_days_ago = today - timedelta(days=7)


def render_ABNRealParam():
    return [
        dcc.Store(id='all-data-pagination', data={"pageSize": 10, "current": 1}),
        dcc.Store(id='alarm-data-pagination', data={"pageSize": 10, "current": 1}),
        html.Div(
            id="ABN-key-param-interval-parent-kjz"
        ),
        html.Div(
            id="ABN-key-param-interval-card-kjz"
        ),
        fac.AntdRow(
            [
                fac.AntdCol(
                    fac.AntdSpace(
                        [
                            fac.AntdCheckboxGroup(
                                id='abn-real-param-kjz-cabin',
                                options=[
                                    {'label': '核心舱', 'value': 'TGTH'},
                                    {'label': '问天舱', 'value': 'TGWT'},
                                    {'label': '梦天舱', 'value': 'TGMT'}
                                ],
                            ),
                        ]
                    ),
                    span=24
                ),

                fac.AntdCol(
                    fac.AntdDivider(
                        "异常参数报警列表",
                        size="small"
                    ),
                    span=24
                ),
                fac.AntdCol(
                    fac.AntdTable(
                        id="abn-real-param-alarm-table-kjz",
                        columns=[
                            {'title': '序号', 'dataIndex': 'Index', 'width': '50px',
                             'renderOptions': {'renderType': 'ellipsis'}, },
                            {'title': '参数代号', 'dataIndex': 'ANOMALY_NO', 'renderOptions': {'renderType': 'ellipsis'}, },
                            {'title': '参数名称', 'dataIndex': 'ANOMALY_NAME',
                             'renderOptions': {'renderType': 'ellipsis'}, },
                            {'title': '载荷', 'dataIndex': 'PAYLOAD_NAME', 'renderOptions': {'renderType': 'ellipsis'}, },
                            {'title': '开始时间', 'dataIndex': 'ALARM_TIME',
                             'renderOptions': {'renderType': 'ellipsis'}, },
                            {'title': '更新时间', 'dataIndex': 'UPDATE_TIME',
                             'renderOptions': {'renderType': 'ellipsis'}, },
                            {'title': '数据来源', 'dataIndex': 'DATA_SOURCE',
                             'renderOptions': {'renderType': 'ellipsis'}, },
                            {'title': '是否结束', 'dataIndex': 'END_FLAG_TAG', 'renderOptions': {'renderType': 'tags'}, },
                            {'title': '标签', 'dataIndex': 'tag'},
                        ],
                        filterOptions={
                            'ANOMALY_NO': {'filterMode': 'keyword'},
                            'ANOMALY_NAME': {'filterMode': 'keyword'},
                            'PAYLOAD_NAME': {'filterSearch': True},
                            'DATA_SOURCE': {'filterSearch': True},
                            'END_FLAG_TAG': {'filterSearch': True},
                        },
                        data=[
                            {"dataIndex": 1, "PAMCode": "dsasdas", "key": 1}
                        ],
                        sortOptions={
                            'sortDataIndexes': [
                                'CREATE_TIME',
                                'UPDATE_TIME',
                            ]
                        },
                        # style={"height": "55vh"},
                        scrollToFirstRowOnChange=False,
                        maxHeight="50vh",
                        pagination={'pageSize': 10},
                        enableCellClickListenColumns=['Index', 'ANOMALY_NO', 'ANOMALY_NAME', 'PAYLOAD_NAME',
                                                      'CREATE_TIME',
                                                      'UPDATE_TIME', 'DATA_SOURCE', 'END_FLAG']
                    ),
                    span=24
                ),
                fac.AntdCol(
                    fac.AntdRow(
                        [

                            fac.AntdCol(
                                dash_echarts.DashECharts(
                                    id="alarm-chart-row-2-child",
                                    option={},
                                    style={"width": "100%", "height": "30vh", "align-items": "center",
                                           "display": "flex"}
                                ),
                                id="alarm-chart-row-2",
                                span=12
                            ),
                            fac.AntdCol(
                                fac.AntdDescriptions(
                                    items=[
                                        {"label": "uuid", "children": "点击上方记录查看报警信息"},
                                        {"label": "参数代号", "children": "点击上方记录查看报警信息"},
                                        {"label": "参数名称", "children": "点击上方记录查看报警信息"},
                                        {"label": "当前阶段判读模式", "children": "点击上方记录查看报警信息"},
                                        {"label": "是否有指令条件	", "children": "点击上方记录查看报警信息"},
                                        {"label": "是否有终止指令	", "children": "点击上方记录查看报警信息"},
                                        {"label": "是否有终止参数规则	", "children": "点击上方记录查看报警信息"},
                                        {"label": "逻辑表达式	", "children": "点击上方记录查看报警信息"},
                                    ],
                                    bordered=True,
                                    size="small",
                                    column=1,
                                    id="alarm-chart-row-3-child",
                                    className="chart-desc",
                                    classNames={
                                        "content": "chart-desc-content-info",
                                    },
                                ),
                                id="alarm-chart-row-3",
                                span=8
                            ),
                            fac.AntdCol(
                                fac.AntdDescriptions(
                                    items=[
                                        {"label": "近期报警个数", "children": ""},
                                        {"label": "待处理包数", "children": ""},
                                        {"label": "总处理包数", "children": ""},
                                        {"label": "处理速率", "children": ""},
                                        {"label": "监测参数总数", "children": ""},
                                        {"label": "CPU占用率", "children": ""},
                                        {"label": "内存占用率", "children": ''}
                                    ],
                                    bordered=True,
                                    size="small",
                                    column=1,
                                    id="alarm-chart-row-1-child",
                                    className="chart-desc",
                                    classNames={
                                        "content": "chart-desc-content",
                                        # "label": "chart-desc-label"
                                    },
                                ),
                                id="alarm-chart-row-1",
                                span=4
                            ),
                        ],
                        id="alarm-chart-row",
                        style={
                            "border": "1px solid #fff",
                            "padding": 10
                        }
                    ),
                    # html.Div(
                    #     id='flip-card',
                    #     className='flip-card',
                    #     children=html.Div(
                    #         id='flip-inner',
                    #         className='flip-card-inner',
                    #         children=[
                    #             # 正面内容
                    #             html.Div([
                    #                 # html.H4("卡片标题", style={'marginBottom': '10px'}),
                    #                 html.P("点击报警记录查看详情")
                    #             ], id='flip-card-front'),
                    #
                    #             # 背面内容
                    #             html.Div([
                    #                 html.H5("详细信息"),
                    #                 html.P("这是更多内容说明。"),
                    #                 fac.AntdButton("操作按钮", size="small")
                    #             ], id='flip-card-back'),
                    #         ]
                    #     ),
                    #     n_clicks=0
                    # ),
                    span=24
                ),
                fac.AntdCol(
                    fac.AntdDivider(
                        "监控参数全局列表",
                        size="small"
                    ),
                    span=24
                ),
                fac.AntdCol(
                    fac.AntdTable(
                        id="abn-real-param-monitor-table-kjz",
                        columns=[
                            {'title': '序号', 'dataIndex': 'dataIndex', 'width': '50px',
                             'renderOptions': {'renderType': 'ellipsis'}, },
                            {'title': '创建时间', 'dataIndex': 'CREATE_TIME',
                             'renderOptions': {'renderType': 'ellipsis'}, },
                            {'title': '参数代号', 'dataIndex': 'ANOMALY_NO', 'renderOptions': {'renderType': 'ellipsis'}, },
                            {'title': '参数名称', 'dataIndex': 'ANOMALY_NAME',
                             'renderOptions': {'renderType': 'ellipsis'}, },
                            {'title': '载荷', 'dataIndex': 'PAYLOAD_NAME', 'renderOptions': {'renderType': 'ellipsis'}, },
                            {'title': '更新时间', 'dataIndex': 'UPDATE_TIME',
                             'renderOptions': {'renderType': 'ellipsis'}, },
                            {'title': '数据来源', 'dataIndex': 'DATA_SOURCE',
                             'renderOptions': {'renderType': 'ellipsis'}, },
                            {'title': '判读状态', 'dataIndex': 'ALARM_STATE',
                             'renderOptions': {'renderType': 'status-badge'}},
                            # {'title': '数据', 'dataIndex': 'data', 'renderOptions': {'renderType': 'mini-line'}, },
                            # {'title': '播放数据', 'dataIndex': 'PLAY_DATA', 'renderOptions': {'renderType': 'switch'}, },
                        ],
                        filterOptions={
                            'ANOMALY_NO': {'filterMode': 'keyword'},
                            'ANOMALY_NAME': {'filterMode': 'keyword'},
                            'PAYLOAD_NAME': {'filterSearch': True},
                            'DATA_SOURCE': {'filterSearch': True},
                            'ALARM_STATE': {'filterSearch': True},
                        },
                        data=[

                        ],
                        loading=False,
                        expandedRowKeys=[],
                        expandedRowKeyToContent=[

                        ],
                        sortOptions={
                            'sortDataIndexes': [
                                'CREATE_TIME',
                                'UPDATE_TIME',
                            ]
                        },
                        # expandRowByClick=True,
                        scrollToFirstRowOnChange=False,
                        maxHeight=500,
                        pagination={
                            'pageSize': 10,
                            'total': 0
                        },
                        enableCellClickListenColumns=['dataIndex', 'PAMName', 'payload', 'PAMCode', 'updateTime',
                                                      'createTime']
                    ),
                    span=24
                ),
            ],
            gutter=10
        ),
    ]
