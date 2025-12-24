import feffery_antd_components as fac
from datetime import datetime
import random
from dash import dcc, html
from dash.dependencies import Input, Output, ClientsideFunction
from openpyxl.styles.builtins import styles
from datetime import datetime, timedelta


from callbacks.ABNReal_c import ABNRealWatch_c

today = datetime.now()
seven_days_ago = today - timedelta(days=7)


def render_ABNRealWatch():
    return [
        fac.AntdRow(
            [
                html.Div(
                    fac.AntdForm(
                        [
                            fac.AntdFormItem(
                                fac.AntdInput(
                                    id='abn-search-anomaly-no-input',
                                    placeholder='请输入故障编号',
                                    autoComplete='off',
                                    allowClear=True,
                                    style={'width': 240},
                                ),
                                label='故障编号',
                                style={
                                    'paddingBottom': '10px'
                                },
                            ),
                            fac.AntdFormItem(
                                fac.AntdInput(
                                    id='abn-search-anomaly-name-input',
                                    placeholder='请输入故障名称',
                                    autoComplete='off',
                                    allowClear=True,
                                    style={'width': 240},
                                ),
                                label='故障名称',
                                style={
                                    'paddingBottom': '10px'
                                },
                            ),
                            fac.AntdFormItem(
                                fac.AntdInput(
                                    id='abn-search-payload-name-input',
                                    placeholder='请输入载荷名称',
                                    autoComplete='off',
                                    allowClear=True,
                                    style={'width': 240},
                                ),
                                label='载荷名称',
                                style={
                                    'paddingBottom': '10px'
                                },
                            ),
                        ],
                        layout='inline',
                        style={
                            'marginLeft': '10px'
                        },
                    )
                )
            ]

        ),
        fac.AntdRow(
            [
                html.Div(
                    fac.AntdForm(
                        [
                            fac.AntdFormItem(
                                fac.AntdDateRangePicker(
                                    id='abn-search-anomaly-date-range-picker',
                                    value=[seven_days_ago.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')]
                                ),
                                label='时间范围',
                                # required=True,
                                style={
                                    'paddingBottom': '10px'
                                },
                            ),
                            fac.AntdFormItem(
                                fac.AntdButton(
                                    '搜索',
                                    id='abn-search-submit-button',
                                    type='primary',
                                    icon=fac.AntdIcon(
                                        icon='antd-search'
                                    ),
                                ),
                                style={
                                    'paddingBottom': '10px'
                                },
                            ),
                            fac.AntdFormItem(
                                fac.AntdButton(
                                    '重置',
                                    id='abn-search-reset-button',
                                    icon=fac.AntdIcon(
                                        icon='antd-sync'
                                    ),
                                ),
                                style={
                                    'paddingBottom': '10px'
                                },
                            ),
                        ],
                        layout='inline',
                        style={
                            'marginLeft': '10px',
                        },
                    )
                )
            ]

        ),
        fac.AntdRow(
            fac.AntdTable(
                id="abn-real-watch-table",
                columns=[
                    {'title': '序号', 'dataIndex': 'dataIndex','width':'50px'},
                    {'title': '故障编号', 'dataIndex': 'ABNNo','renderOptions': {'renderType': 'ellipsis'}},
                    {'title': '故障名称', 'dataIndex': 'ABNName','renderOptions': {'renderType': 'ellipsis'}},
                    {'title': '载荷名称', 'dataIndex': 'payload','renderOptions': {'renderType': 'ellipsis'}},
                    {'title': '开始时间', 'dataIndex': 'startTime','renderOptions': {'renderType': 'ellipsis'}},
                    {'title': '更新时间', 'dataIndex': 'updateTime','renderOptions': {'renderType': 'ellipsis'}},
                    {'title': '规则版本', 'dataIndex': 'ruleVersion',
                     'renderOptions': {'renderType': 'tags'}, }
                ],
                filterOptions={
                    'ABNNo': {'filterMode': 'keyword'},
                    'ABNName': {'filterMode': 'keyword'},
                    'payload': {'filterSearch': True},
                    'ruleVersion': {}
                },
                sortOptions={
                    'sortDataIndexes': [
                        'startTime',
                        'updateTime',
                    ]
                },
                scrollToFirstRowOnChange=False,
                maxHeight=500,
                pagination={'pageSize': 15},
                enableCellClickListenColumns=['dataIndex', 'ABNName', 'payload', 'startTime', 'updateTime',
                                              'ruleVersion']
            ),
        )
    ]
