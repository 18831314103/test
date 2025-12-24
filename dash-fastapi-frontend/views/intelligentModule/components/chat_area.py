from dash import html, dcc
import feffery_antd_components as fac
import feffery_utils_components as fuc

from views.intelligentModule.components.chat_message_box import chat_message_box
from views.intelligentModule.components.config import AppConfig


def chat_area(conversation_id: str):
    """渲染对话区域"""

    return html.Div(
        [
            # 记录用户最新一次发送的原始问题信息
            dcc.Store(id="newest-user-input"),
            # 记录当前最新任务信息
            dcc.Store(id="current-running-task-info"),
            # 聊天消息列表像素高度监听
            fuc.FefferyListenElementSize(
                id="listen-chat-area-list-height", target="chat-area-list"
            ),
            fac.AntdSpace(
                # 初始化系统提示语
                [
                    chat_message_box(
                        conversation_id=conversation_id,
                        role="system",
                        system_prompt=AppConfig.initial_system_prompt,
                        message_uuid="system-initial",
                    )
                ],
                id="chat-area-list",
                direction="vertical",
                style={"width": "100%"},
            ),
        ],
        id="chat-area",
    )
