from dash import set_props
import feffery_antd_components as fac
import feffery_utils_components as fuc
import uuid
import dash
from flask import Response, request
from server import app
from dash.dependencies import Input, Output, State, ClientsideFunction
import time
import json
from openai import OpenAI


@app.callback(
    [
        Output("question-chat", "data"),
        Output("answer-content", "markdownStr"),
    ],
    Input("submit", "nClicks"),
    State("question", "value"),
    prevent_initial_call=True,
)
def create_new_sse(nClicks, question):
    if not question:
        # 如果没有输入问题，给出警告
        set_props(
            "global-message",
            {
                "children": fac.AntdMessage(
                    content="请填写有效的问题",
                    type="warning",
                )
            },
        )
        set_props("submit", {"loading": False})
        return [dash.no_update, dash.no_update]
    return [
        question,
        "",  # 重置内容
    ]


# @app.callback(
#     [
#         Output("answer-content", "markdownStr", allow_duplicate=True),
#     ],
#     Input("deepseek-stream", "data"),
#     [State("answer-content", "markdownStr")],
#     prevent_initial_call=True,
# )
# def render_data(data, markdown):
#     print(data)
#
#     if data != None:
#
#         return [markdown + data]
#     else:
#         return [markdown]
@app.callback(
    [
        Output("answer-content", "markdownStr", allow_duplicate=True),
    ],
    Input("answer-chat", "data"),
    State("question", "value"),
    prevent_initial_call=True,
)
def render_answer(answer, question):
    return [answer]


app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="updateResponse"),
    Input("question-chat", "data"),
    State("answer-content", "markdownStr"),
    prevent_initial_call=True,
)
