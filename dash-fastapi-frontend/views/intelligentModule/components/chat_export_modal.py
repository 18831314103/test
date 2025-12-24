from dash import html, dcc
import feffery_antd_components as fac


def chat_export_modal():
    """渲染对话导出模态框"""

    return fac.AntdModal(
        html.Div(
            [
                fac.AntdForm(
                    [
                        fac.AntdFormItem(
                            fac.AntdSelect(
                                id="chat-export-format",
                                options=["markdown", "json"],
                                value="markdown",
                                allowClear=False,
                            ),
                            label="导出格式",
                        ),
                    ],
                    layout="vertical",
                    style={"padding": 12},
                ),
                # 处理导出结果下载
                dcc.Download(id="chat-export-download"),
            ],
            className="chat-export-container",
        ),
        id="chat-export-modal",
        title=fac.AntdSpace(
            [
                fac.AntdText("对话导出", strong=True, style={"fontSize": 20}),
                fac.AntdText(
                    "将当前对话记录导出为多种格式的结果",
                    style={"fontWeight": "normal", "fontSize": 14},
                ),
            ],
            direction="vertical",
            size=0,
        ),
        destroyOnClose=False,
        renderFooter=True,
        okText="确认导出",
        confirmAutoSpin=True,
        loadingOkText="导出中",
        okClickClose=False,
    )
