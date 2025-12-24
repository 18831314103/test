import uuid
import dash
import time
import json
from openai import OpenAI
from dash import set_props, dcc,html
from flask import Response, request
import feffery_antd_components as fac
import feffery_utils_components as fuc
import feffery_markdown_components as fmc
from dash.dependencies import Input, Output, State, ClientsideFunction
from callbacks.intelligentModule_c import chat_c_new
from server import app
from conversation_cache import conversation_cache
from views.intelligentModule.components.header_bar import header_bar
from views.intelligentModule.components.chat_area import chat_area
from views.intelligentModule.components.input_area import input_area
from views.intelligentModule.components.setting_modal import setting_modal
from views.intelligentModule.components.chat_export_modal import chat_export_modal

def render(*args, **kwargs):
    # # 生成唯一识别对话id
    conversation_id = str(uuid.uuid4())
    #
    # # 初始化当前对话缓存
    conversation_cache.insert(
        conversation_id,
        [],
    )
    return [
        fac.AntdConfigProvider(
            [
                # 分配唯一对话id
                dcc.Store(id="conversation-id", data=conversation_id),
                # 页面重载或关闭事件监听
                fuc.FefferyListenUnload(id="listen-unload"),
                # 全局消息提示
                fac.Fragment(id="global-message"),
                fac.AntdCenter(
                    [
                        # 对话框容器
                        html.Div(
                            [
                                # 顶部栏
                                header_bar(),
                                # # 对话区域
                                chat_area(conversation_id),
                                # # 底部输入区域
                                input_area(),
                            ],
                            id="chat-container",
                            style={
                                "width": "90vw",
                                "height": "85vh",
                                "maxWidth": 1200,
                                "borderRadius": 16,
                                "marginBottom":40,
                                "border": "1px solid #dedede",
                            },
                        ),
                        # 设置中心模态框
                        setting_modal(),
                        # 对话导出模态框
                        chat_export_modal(),
                    ],
                    style={"padding": 10,"overflow":"auto"},
                ),
            ]
        )
    ]
