import json
import time
import dash
from datetime import datetime
from dash import Patch, set_props
import feffery_antd_components as fac
from dash.dependencies import Input, Output, State, MATCH, ClientsideFunction
from server import app
from views.intelligentModule.components.config import AppConfig
from views.intelligentModule.components.chat_message_box import chat_message_box
from conversation_cache import conversation_cache


@app.callback(Input("listen-unload", "unloaded"), State("conversation-id", "data"))
def clear_conversation_cache(unloaded, conversation_id):
    """在页面刷新或关闭时，清除对应的对话缓存数据"""

    if conversation_cache.get(conversation_id):
        del conversation_cache[conversation_id]


app.clientside_callback(
    # 处理对话框整体的全屏/退出全屏
    ClientsideFunction(
        namespace="chat_clientside", function_name="handleChatContainerFullscreen"
    ),
    [
        Output("chat-container-full-screen-icon", "icon"),
        Output("chat-container", "style"),
    ],
    Input("chat-container-full-screen", "nClicks"),
    State("chat-container-full-screen-icon", "icon"),
    prevent_initial_call=True,
)

app.clientside_callback(
    # 控制对话消息框的显示/隐藏
    ClientsideFunction(
        namespace="chat_clientside", function_name="handleOperationButtonGroupVisible"
    ),
    Output(
        {
            "type": "operation-button-group",
            "index": MATCH,
        },
        "style",
    ),
    Input(
        {"type": "chat-message-box-listen-hover", "index": MATCH},
        "isHovering",
    ),
    State(
        {
            "type": "operation-button-group",
            "index": MATCH,
        },
        "style",
    ),
    prevent_initial_call=True,
)

app.clientside_callback(
    # 控制用户信息输入框内容的发送
    ClientsideFunction(
        namespace="chat_clientside", function_name="handleUserNewMessageSend"
    ),
    [Output("newest-user-input", "data"), Output("input-text", "value")],
    [
        Input("shift-enter-keypress", "pressedCounts"),
        Input("enter-keypress", "pressedCounts"),
        Input("send-input-text", "nClicks"),
    ],
    State("input-text", "value"),
    prevent_initial_call=True,
)


@app.callback(
    [
        Output("chat-area-list", "children"),
        Output("send-input-text", "loading"),
        Output("input-text", "disabled"),
    ],
    [
        Input("newest-user-input", "data"),
        Input("chat-area-clear", "nClicks"),
        Input("chat-setting-model", "value"),
    ],
    [
        State("conversation-id", "data"),
        State("chat-setting-temperature", "value"),
        State("chat-setting-max-tokens", "value"),
    ],
    prevent_initial_call=True,
)
def append_new_user_input(
        new_question, nClicks, current_model, conversation_id, temperature, max_tokens
):
    """处理新发送问题对话信息框的追加，或清空聊天记录操作"""

    if dash.ctx.triggered_id == "newest-user-input":
        # 尝试提取有效的模型厂商、子模型名称
        if "|" in current_model:
            model_name = current_model.split("|")[0]
            sub_model_name = current_model.split("|")[1]
        else:
            model_name = None
            sub_model_name = None

        p = Patch()

        p.extend(
            [
                chat_message_box(
                    conversation_id=conversation_id,
                    role="user",
                    user_input_text=new_question,
                ),
                chat_message_box(
                    conversation_id=conversation_id,
                    role="assistant",
                    user_input_text=new_question,
                    model_name=model_name,
                    sub_model_name=sub_model_name,
                    temperature=temperature,
                    max_tokens=max_tokens,
                ),
            ]
        )

        return p, True, True

    # “清空聊天”按钮被点击，或当前模型发生切换时，均需要重新初始化当前对话缓存
    elif dash.ctx.triggered_id in ["chat-area-clear", "chat-setting-model"]:
        # 初始化当前对话缓存
        # conversation_cache.insert(
        #     conversation_id,
        #     [],
        # )

        return [
            # 初始化系统提示语
            [
                chat_message_box(
                    conversation_id=conversation_id,
                    role="system",
                    system_prompt=AppConfig.initial_system_prompt,
                    message_uuid="system-initial",
                )
            ],
            False,
            False,
        ]


# @app.callback(
#     [Output(
#         {
#             "type": "assistant-output-markdown",
#             "index": MATCH,
#         },
#         "markdownStr",
#     ), ],
#     [Input({
#         "type": "assistant-output-sse",
#         "index": MATCH,
#     }, 'data')],
#     prevent_initial_call=True
# )
# def accumulate(message):
#     print(message)
#     if not message:
#         return ["等待数据..."]
#
#     try:
#         data = json.loads(message)
#         time.sleep(0.5)
#         return [data]
#
#     except json.JSONDecodeError:
#         return ["无效的数据格式"]


app.clientside_callback(
    # 处理流式回复内容更新相关过程
    ClientsideFunction(namespace="chat_clientside", function_name="handleStreamResponse"),
    [
        Output(
            {
                "type": "assistant-output-markdown",
                "index": MATCH,
            },
            "children",
        ),
    ],
    Input(
        {
            "type": "assistant-output-store",
            "index": MATCH,
        },
        "data",
    ),
    # prevent_initial_call=True,
)

app.clientside_callback(
    # 处理聊天区域的自动滚动策略
    ClientsideFunction(namespace="chat_clientside", function_name="handleChatAreaScroll"),
    Input("listen-chat-area-list-height", "height"),
    State("enable-auto-scroll", "checked"),
)

app.clientside_callback(
    # 处理工具按钮条中的“前往顶部”、“回到底部”操作
    ClientsideFunction(
        namespace="chat_clientside", function_name="handleChatAreaToTopBottom"
    ),
    [
        Input("chat-area-to-top", "nClicks"),
        Input("chat-area-to-bottom", "nClicks"),
    ],
)

app.clientside_callback(
    # 处理ai回复消息框“中断”按钮操作
    ClientsideFunction(
        namespace="chat_clientside", function_name="handleAssistantOutputStop"
    ),
    Output(
        {
            "type": "assistant-output-sse",
            "index": MATCH,
        },
        "operation",
    ),
    Input(
        {
            "type": "assistant-output-stop",
            "index": MATCH,
        },
        "nClicks",
    ),
    prevent_initial_call=True,
)

app.clientside_callback(
    # 处理ai回复消息框“重试”按钮操作
    ClientsideFunction(
        namespace="chat_clientside", function_name="handleAssistantOutputRetry"
    ),
    [
        Output(
            {
                "type": "assistant-output-markdown",
                "index": MATCH,
            },
            "markdownStr",
            allow_duplicate=True,
        ),
        Output(
            {
                "type": "assistant-output-markdown",
                "index": MATCH,
            },
            "children",
            allow_duplicate=True,
        ),
        Output(
            {
                "type": "assistant-output-sse",
                "index": MATCH,
            },
            "key",
        ),
    ],
    Input(
        {
            "type": "assistant-output-retry",
            "index": MATCH,
        },
        "nClicks",
    ),
    prevent_initial_call=True,
)

app.clientside_callback(
    # 处理ai回复消息框“赋值 ”按钮操作
    ClientsideFunction(
        namespace="chat_clientside", function_name="handleAssistantOutputCopy"
    ),
    Output(
        {
            "type": "assistant-output-copy",
            "index": MATCH,
        },
        "id",
    ),
    Input(
        {
            "type": "assistant-output-copy",
            "index": MATCH,
        },
        "nClicks",
    ),
    State(
        {
            "type": "assistant-output-markdown",
            "index": MATCH,
        },
        "markdownStr",
    ),
    prevent_initial_call=True,
)

app.clientside_callback(
    # 更新标题栏显示的“当前模型”
    ClientsideFunction(namespace="chat_clientside", function_name="showCurrentModel"),
    Output("header-bar-current-model", "children"),
    Input("chat-setting-model", "value"),
)

app.clientside_callback(
    # 更新标题栏显示的“对话数量”,
    """(children) => `共 ${children.length} 条对话`""",
    Output("header-bar-chat-message-count", "children"),
    Input("chat-area-list", "children"),
)


@app.callback(
    [
        Output("chat-export-download", "data"),
        Output("chat-export-modal", "confirmLoading"),
    ],
    Input("chat-export-modal", "okCounts"),
    [State("conversation-id", "data"), State("chat-export-format", "value")],
    prevent_initial_call=True,
)
def handle_chat_export(okCounts, conversation_id, export_format):
    """处理当前聊天记录的导出"""

    time.sleep(0.5)

    # 查询当前对话id对应的完整对话记录
    chat_records = conversation_cache.get(conversation_id)

    if export_format == "json":
        set_props(
            "global-message",
            {"children": fac.AntdMessage(type="success", content="导出成功")},
        )
        return [
            dict(
                content=json.dumps(chat_records, ensure_ascii=False, indent=4),
                filename="对话导出{}.json".format(
                    datetime.now().strftime("%Y%m%d%H%M%S")
                ),
            ),
            False,
        ]

    elif export_format == "markdown":
        markdown_str = ""

        for record in chat_records:
            markdown_str += "> role: " + record["role"] + "\n\n"
            markdown_str += record.get("content") + "\n\n---\n\n"

        set_props(
            "global-message",
            {"children": fac.AntdMessage(type="success", content="导出成功")},
        )
        return [
            dict(
                content=markdown_str,
                filename="对话导出{}.md".format(
                    datetime.now().strftime("%Y%m%d%H%M%S")
                ),
            ),
            False,
        ]

    return dash.no_update
