from datetime import datetime
import random
from dash import dcc, html
from dash.dependencies import Input, Output, ClientsideFunction
from openpyxl.styles.builtins import styles
import feffery_antd_components as fac
import feffery_utils_components as fuc
from callbacks.ABNReal_c import ABNRealModule_c


def render_ABNRealModule():
    return [
        html.Div(
            id="ABN-interval-parent"
        ),
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='ABN-real-module-store'),
        dcc.Store(id='ABN-real-module-store-clicktable'),
        dcc.Store(id='ABN-real-module-store-clicktable-data'),
        dcc.Store(id='ABN-real-module-store-clicktable-dataDesc'),
        dcc.Store(id='ABN-real-module-store-no-output'),
        dcc.Store(id='ABN-Check-YC-Modal-store'),
        fuc.FefferyFullscreen(
            id='fullscreen-gojs',
            targetId='ABN-real-module-gojs'
        ),
        fac.AntdButton(
            "误报管理",
            id="ABN-real-module-warn-manager",
            style={"marginBottom":10,"float":"right"}
        ),
        html.Div(
            fac.AntdTable(
                id="ABN-real-module-table",
                columns=[
                    {'title': '序号', 'dataIndex': 'dataIndex', 'width': '50px','renderOptions': {'renderType': 'ellipsis'},},
                    {'title': '故障编号', 'dataIndex': 'ABNNo', 'width': '150px','renderOptions': {'renderType': 'ellipsis'},},
                    {'title': '故障名称', 'dataIndex': 'ABNName', 'width': '200px','renderOptions': {'renderType': 'ellipsis'},},
                    {'title': '载荷名称', 'dataIndex': 'payload','renderOptions': {'renderType': 'ellipsis'},},
                    {'title': '开始时间', 'dataIndex': 'startTime','width': '150px','renderOptions': {'renderType': 'ellipsis'},},
                    {'title': '更新时间', 'dataIndex': 'updateTime','width': '150px','renderOptions': {'renderType': 'ellipsis'},},
                    {'title': '数据来源', 'dataIndex': 'DATA_SOURCE', 'width': '150px','renderOptions': {'renderType': 'ellipsis'},},
                    # {'title': '规则版本', 'dataIndex': 'ruleVersion',
                    #  'renderOptions': {'renderType': 'tags'}, 'width': '150px'},
                    {'title': '状态', 'dataIndex': 'readStatusText',
                     'renderOptions': {'renderType': 'ellipsis'}},
                    {'title': '是否结束', 'dataIndex': 'END_FLAG', 'width': '150px','renderOptions': {'renderType': 'ellipsis'},},
                    {
                        'title': '操作',
                        'dataIndex': 'action',
                        'renderOptions': {'renderType': 'button'},
                    },
                ],
                filterOptions={
                    'ABNNo': {'filterMode': 'keyword'},
                    'ABNName': {'filterMode': 'keyword'},
                    'payload': {'filterSearch': True},
                    'ruleVersion': {},
                    'DATA_SOURCE': {},
                    'END_FLAG': {}
                },
                sortOptions={
                    'sortDataIndexes': [
                        # 'startTime',
                        'updateTime',
                    ],
                    # 'orders':['descend']
                },
                #bordered=True,
                scrollToFirstRowOnChange=False,
                maxHeight="calc(100vh - 500px)",
                # virtual=True,
                # style={"height":"calc(100vh - 500px)"},
                pagination={'pageSize': 10, 'hideOnSinglePage': True},
                enableCellClickListenColumns=['dataIndex', 'ABNName', 'payload', 'startTime', 'updateTime',
                                              'DATA_SOURCE', 'ruleVersion', 'END_FLAG', 'action']
            ),
        ),
        html.Div(
            fuc.FefferyRawHTML(
                id='statistic-info-text'
            ),
            style={
                'textAlign': 'right',
            }
        ),
        fac.AntdDivider(

            # id='statistic-info-text',
            size="small"
        ),
        html.Div(
            [

                fac.AntdRow(
                    [
                        fac.AntdCol(
                            [
                                html.Div(
                                    [
                                        fac.AntdButton(
                                            '全屏显示',
                                            type='primary',
                                            id='fullscreen-gojs-button',
                                            style={
                                                "position": "absolute",
                                                "top": 20,
                                                "right": 20,
                                                "zIndex": 10
                                            }
                                        ),
                                        fac.AntdButton(
                                            '判据描述信息',
                                            id='fullscreen-gojs-title',
                                            style={
                                                "position": "absolute",
                                                "top": 20,
                                                "left": 20,
                                                "zIndex": 10,
                                                "background":"#373e45",
                                                "padding":6
                                            }
                                        ),
                                        html.Div(
                                            id="ABN-real-module-gojs",
                                            style={
                                                "height": 300,
                                                "border": "1px solid #303030",
                                                "overflowY": "hidden",
                                            }

                                        )
                                    ]
                                ),

                            ],
                            span=16
                        ),
                        fac.AntdCol(
                            [
                                fac.AntdCard(
                                    html.Div(
                                        id="ABNReal-recent-record-card",
                                        style={
                                            'width': '100%',
                                            "height": 240,
                                            "overflowY": "auto",
                                        },
                                    ),
                                    size='small',
                                    title='近期报警记录',
                                    # bordered=False,
                                    style={
                                        'marginBottom': '24px',
                                    },
                                ),
                            ],
                            span=8,
                        )
                    ],
                    style={

                        # 'height': 160,
                        "marginTop": 10,
                        "overflowY": "hidden"
                    },
                    gutter=10,
                ),

            ],
            style={
                'paddingTop': 5,
            }
        ),
        # html.Div(
        #     id="ABN-real-module-chart",
        #     style={
        #         # 'background': f'rgba(28, 126, 214, calc(0.8))',
        #         'height': 130,
        #         "background": "#D9EDF6",
        #         # "boxShadow": "rgb(240, 241, 242) 0px 2px 14px",
        #         'borderTop': '2px dashed grey'
        #     },
        # ),
    ]
