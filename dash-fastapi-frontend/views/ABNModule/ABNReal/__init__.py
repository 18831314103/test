import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import dcc, html
from datetime import datetime
import plotly.express as px
import pandas as pd
from server import app
from dash.dependencies import Input, Output, State
import random
from views.ABNModule.ABNReal.ABNRealModule import render_ABNRealModule
from views.ABNModule.ABNReal.ABNRealRecord import render_ABNRealRecord
from views.ABNModule.ABNReal.ABNRealWatch import render_ABNRealWatch
from views.ABNModule.ABNReal.ABNCheckYCModal import render_check_YC_modal
data = {
    'City': ['A', 'B', 'C', 'D', 'E'],
    'Product A': [10, 15, 7, 12, 5],
    'Product B': [5, 10, 14, 8, 13]
}

df = pd.DataFrame(data)
def render(*args, **kwargs):
    return [
        # fuc.FefferyWebSocket(
        #     id='websocket',
        #     socketUrl='ws://10.2.28.37:8083/mqtt'
        # ),
        # fac.AntdParagraph(
        #     id='websocket-demo-state'
        # ),
        html.Div(
            [
                fac.AntdTabs(
                    items=[
                        {
                            'key': f'故障模式实时报警',
                            'label': f'故障模式实时报警',
                            'children':render_ABNRealModule(),
                        },
                        {
                            'key': f'故障模式全局监控',
                            'label': f'故障模式全局监控',
                            'children': render_ABNRealRecord()
                        },
                        {
                            'key': f'故障模式处置记录',
                            'label': f'故障模式处置记录',
                            'children': render_ABNRealWatch(),
                        }
                    ],
                    id="ABNMode-Tabs",
                ),
                render_check_YC_modal()[0]
            ],
            style={'padding':10,
                   # 'background':'#D9EDF6',
                   'marginLeft':-15,'width':'calc(100% + 10px)'},
            id="ABNMode",
        )

    ]
# app.clientside_callback(
#     '''(state) => `state: ${state}`''',
#     # Output('websocket-demo-state', 'children'),
#     Input('websocket', 'state')
# )