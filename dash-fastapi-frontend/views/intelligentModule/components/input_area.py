from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc


def input_area():
    """渲染用户输入区域"""

    return html.Div(
        [
            # 工具按钮条
            fac.AntdSpace(
                [
                    fac.AntdCheckableTag(
                        id="enable-auto-scroll",
                        checked=True,
                        checkedContent="自动滚动开",
                        unCheckedContent="自动滚动关",
                        className="tool-button-container-tag",
                    ),
                    fac.AntdButton(
                        "前往顶部",
                        id="chat-area-to-top",
                        icon=fac.AntdIcon(icon="antd-up"),
                        shape="round",
                        size="small",
                    ),
                    fac.AntdButton(
                        "回到底部",
                        id="chat-area-to-bottom",
                        icon=fac.AntdIcon(icon="antd-down"),
                        shape="round",
                        size="small",
                    ),
                    fac.AntdButton(
                        "清空聊天",
                        id="chat-area-clear",
                        icon=fac.AntdIcon(icon="antd-clear"),
                        shape="round",
                        size="small",
                    ),
                    # fac.AntdTooltip(
                    #     fac.AntdButton(
                    #         "上传附件",
                    #         icon=fac.AntdIcon(icon="antd-cloud-upload"),
                    #         shape="round",
                    #         size="small",
                    #         disabled=True,
                    #     ),
                    #     title="功能开发中",
                    # ),
                ],
                id="tool-button-container",
                wrap=True,
                align="center",
                style={
                    "position": "absolute",
                    "top": 12,
                    "left": 24,
                },
            ),
            # shift+enter事件监听
            fuc.FefferyKeyPress(id="shift-enter-keypress", keys="shift.enter"),
            # enter事件监听
            fuc.FefferyKeyPress(id="enter-keypress", keys="enter"),
            # 对话输入框
            fac.AntdInput(
                id="input-text",
                placeholder="Enter 发送，Shift + Enter 换行",
                mode="text-area",
                autoSize={"minRows": 4, "maxRows": 4},
                style={
                    "position": "absolute",
                    "bottom": 8,
                    "right": 20,
                    "width": "calc(100% - 40px)",
                },
            ),
            # 对话发送按钮
            fac.AntdButton(
                "发送",
                id="send-input-text",
                icon=fac.AntdIcon(icon="antd-export"),
                type="primary",
                size="large",
                loadingChildren="输出中",
                style={
                    "position": "absolute",
                    "right": 36,
                    "bottom": 20,
                },
            ),
        ],
        id="input-area",
    )
