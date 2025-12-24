import feffery_antd_components as fac


def header_bar():
    """渲染顶部栏"""

    return fac.Fragment(
        [
            fac.AntdRow(
                [
                    # 标题信息
                    fac.AntdCol(
                        fac.AntdCenter(
                            fac.AntdSpace(
                                [
                                    fac.AntdSpace(
                                        [
                                            fac.AntdText(
                                                "新的聊天",
                                                style={
                                                    "fontSize": 20,
                                                    "fontWeight": "bolder",
                                                },
                                            ),
                                            fac.AntdText(
                                                "当前模型：",
                                                id="header-bar-current-model",
                                                type="secondary",
                                                style={
                                                    "fontSize": 14,
                                                },
                                            ),
                                        ],
                                        align="end",
                                    ),
                                    fac.AntdText(
                                        "共 1 条对话",
                                        id="header-bar-chat-message-count",
                                        style={"fontSize": 14},
                                    ),
                                ],
                                direction="vertical",
                                size=0,
                            ),
                            style={"height": "100%"},
                        )
                    ),
                    # 操作按钮
                    fac.AntdCol(
                        fac.AntdCenter(
                            fac.AntdSpace(
                                [
                                    fac.AntdButton(
                                        id="open-chat-setting-modal",
                                        icon=fac.AntdIcon(
                                            icon="antd-setting",
                                        ),
                                        size="large",
                                        title="设置中心",
                                        clickExecuteJsString="window.dash_clientside.set_props('chat-setting-modal', { visible: true })",
                                    ),
                                    fac.AntdButton(
                                        id="open-chat-export-modal",
                                        icon=fac.AntdIcon(
                                            icon="antd-download",
                                        ),
                                        size="large",
                                        title="导出对话",
                                        clickExecuteJsString="window.dash_clientside.set_props('chat-export-modal', { visible: true })",
                                    ),
                                    fac.AntdButton(
                                        id="chat-container-full-screen",
                                        icon=fac.AntdIcon(
                                            id="chat-container-full-screen-icon",
                                            icon="antd-full-screen",
                                        ),
                                        size="large",
                                        title="切换全屏",
                                    ),
                                ]
                            ),
                            style={"height": "100%"},
                        )
                    ),
                ],
                justify="space-between",
                align="middle",
                id="header-bar",
            )
        ]
    )
