import uuid
from dash import html, dcc
from datetime import datetime
from typing import Literal, Union
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash.dependencies import Component
import feffery_markdown_components as fmc

from conversation_cache import conversation_cache


# from dash_extensions import EventSource


def chat_message_box(
        conversation_id: str,
        role: Literal["system", "user", "assistant"],
        system_prompt: Union[str, Component] = None,
        user_input_text: str = None,
        message_uuid: str = None,
        model_name: str = None,
        sub_model_name: str = None,
        temperature: float = 0.5,
        max_tokens: int = 4000,
):
    """渲染不同角色的对话消息框"""

    # 生成当前消息框唯一uuid
    new_uuid = message_uuid or str(uuid.uuid4())

    # 开场系统提示对话消息框
    if role == "system":
        # 更新当前对话缓存
        conversation_cache.update(
            {
                conversation_id: [
                    {
                        "role": "system",
                        "content": system_prompt,
                        "message_id": new_uuid,
                    },
                ]
            }
        )

        return fac.AntdRow(
            fac.AntdCol(
                fac.AntdFlex(
                    [
                        fac.AntdAvatar(
                            mode="icon",
                            icon="antd-robot",
                            style={"background": "#1677ff"},
                        ),
                        html.Div(
                            [
                                system_prompt,
                                html.Div(
                                    datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                                    className="chat-message-box-datetime-left",
                                ),
                            ],
                            style={
                                "background": "#f2f2f2",
                            },
                            className="chat-message-box",
                        ),
                    ],
                    vertical=True,
                    align="start",
                    gap=8,
                    style={"width": "100%"},
                ),
                span=20,
                style={"position": "relative"},
            ),
            justify="start",
        )

    # 用户输入对话消息框
    elif role == "user":
        # 更新当前对话缓存
        conversation_cache.update(
            {
                conversation_id: [
                    *conversation_cache.get(conversation_id),
                    {
                        "role": "user",
                        "content": user_input_text,
                        "message_id": new_uuid,
                    },
                ]
            }
        )

        return fac.AntdRow(
            fac.AntdCol(
                fac.AntdFlex(
                    [
                        fac.AntdAvatar(
                            mode="icon",
                            icon="antd-user",
                            style={"background": "#1677ff"},
                        ),
                        html.Div(
                            [
                                fac.AntdText(user_input_text, copyable=True),
                                html.Div(
                                    datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                                    className="chat-message-box-datetime-right",
                                ),
                            ],
                            style={
                                "background": "#e6f7ff",
                            },
                            className="chat-message-box",
                        ),
                    ],
                    vertical=True,
                    align="end",
                    gap=8,
                    style={"width": "100%"},
                ),
                span=20,
                style={"position": "relative"},
            ),
            justify="end",
        )

    # ai回复对话消息框
    elif role == "assistant":
        return html.Div(
            fac.AntdRow(
                fac.AntdCol(
                    fac.AntdFlex(
                        [
                            fac.AntdAvatar(
                                mode="icon",
                                icon="antd-robot",
                                style={"background": "#1677ff"},
                            ),
                            html.Div(
                                [
                                    # 鼠标悬停监听
                                    fuc.FefferyListenHover(
                                        id={
                                            "type": "chat-message-box-listen-hover",
                                            "index": new_uuid,
                                        },
                                        targetSelector=".{}".format(
                                            "chat-message-box-" + new_uuid
                                        ),
                                    ),
                                    dcc.Store(
                                        id={
                                            "type":"assistant-output-store",
                                            "index":new_uuid
                                        },
                                        data={
                                            'model_name':model_name,
                                            'sub_model_name':sub_model_name,
                                            'temperature':temperature,
                                            'max_tokens':max_tokens,
                                            'session_id':conversation_id,
                                            'message_id':new_uuid,
                                            'user_input_text':user_input_text,
                                            'mode':"chat"
                                        }
                                    ),
                                    # 流式问题请求监听
                                    # fuc.FefferyEventSource(
                                    #     id={
                                    #         "type": "assistant-output-sse",
                                    #         "index": new_uuid,
                                    #     },
                                    #
                                    #     url=(
                                    #         "http://localhost:9099/streaming?model_name={}&sub_model_name={}&temperature={}&max_tokens={}&session_id={}&message_id={}&message={}&mode={}".format(
                                    #             model_name,
                                    #             sub_model_name,
                                    #             temperature,
                                    #             max_tokens,
                                    #             conversation_id,
                                    #             new_uuid,
                                    #             user_input_text,
                                    #             "chat"
                                    #         )
                                    #         if model_name and sub_model_name
                                    #         else "http://localhost:9099/streaming?session_id={}&message_id={}&message={}&mode={}".format(
                                    #             conversation_id,
                                    #             new_uuid,
                                    #             user_input_text,
                                    #             "chat"
                                    #         )
                                    #     ),
                                    # ),
                                    fmc.FefferyMarkdown(
                                        id={
                                            "type": "assistant-output-markdown",
                                            "index": new_uuid,
                                        },
                                        markdownStr="",
                                        # placeholder=fuc.FefferyExtraSpinner(
                                        #     type="ball"
                                        # ),
                                        codeTheme="dracula",
                                        codeBlockStyle={
                                            "overflowX": "auto",
                                        },
                                        style={
                                            "background": "transparent",
                                            "fontSize": 14,
                                        },
                                    ),
                                    html.Div(
                                        datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                                        className="chat-message-box-datetime-left",
                                    ),
                                    # 工具按钮条
                                    fac.AntdSpace(
                                        [
                                            fac.AntdButton(
                                                "中断",
                                                id={
                                                    "type": "assistant-output-stop",
                                                    "index": new_uuid,
                                                },
                                                icon=fac.AntdIcon(icon="antd-stop"),
                                                shape="round",
                                                size="small",
                                            ),
                                            fac.AntdButton(
                                                "重试",
                                                id={
                                                    "type": "assistant-output-retry",
                                                    "index": new_uuid,
                                                },
                                                icon=fac.AntdIcon(icon="antd-sync"),
                                                shape="round",
                                                size="small",
                                            ),
                                            fac.AntdButton(
                                                "复制",
                                                id={
                                                    "type": "assistant-output-copy",
                                                    "index": new_uuid,
                                                },
                                                icon=fac.AntdIcon(icon="antd-copy"),
                                                shape="round",
                                                size="small",
                                            ),
                                        ],
                                        id={
                                            "type": "operation-button-group",
                                            "index": new_uuid,
                                        },
                                        className="operation-button-group",
                                        style={
                                            "position": "absolute",
                                            "top": -36,
                                            "left": 40,
                                            "opacity": 0,
                                            "transform": "scale(1) translateY(0)",
                                        },
                                    ),
                                ],
                                style={
                                    "background": "#f2f2f2",
                                },
                                className="chat-message-box",
                            ),
                        ],
                        vertical=True,
                        align="start",
                        gap=8,
                        style={"width": "100%"},
                    ),
                    span=20,
                    style={"position": "relative"},
                ),
                justify="start",
            ),
            id={"type": "chat-message-box", "index": new_uuid},
            className="chat-message-box-" + new_uuid,
        )
