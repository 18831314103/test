import feffery_antd_components as fac
from dash import dcc, html
import pandas as pd
from views.ABNModuleKjz.ABNReal.ABNRealModule import render_ABNRealModule
from views.ABNModuleKjz.ABNReal.ABNRealRecord import render_ABNRealRecord
from views.ABNModuleKjz.ABNReal.ABNRealWatch import render_ABNRealWatch
from views.ABNModuleKjz.ABNReal.ABNRealParam import render_ABNRealParam
from views.ABNModuleKjz.ABNReal.ABNCheckYCModal import render_check_YC_modal
data = {
    'City': ['A', 'B', 'C', 'D', 'E'],
    'Product A': [10, 15, 7, 12, 5],
    'Product B': [5, 10, 14, 8, 13]
}

df = pd.DataFrame(data)
def render(*args, **kwargs):
    return [

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
                        },
                        {
                            'key': f'关键参数异常检测',
                            'label': f'关键参数异常检测',
                            'children': render_ABNRealParam(),
                        }
                    ],
                    id="ABNMode-Tabs-kjz",
                ),
                render_check_YC_modal()[0]
            ],
            style={'padding':10,
                   # 'background':'#D9EDF6',
                   'marginLeft':-15,'width':'calc(100% + 10px)'},
            id="ABNMode-kjz",
        )

    ]
