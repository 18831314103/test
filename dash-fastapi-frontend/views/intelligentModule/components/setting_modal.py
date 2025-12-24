from dash import html
import feffery_antd_components as fac

from views.intelligentModule.components.config import ModelsConfig


def models_check_cards():
    """基于配置参数渲染模型选择卡片"""

    children = [
        fac.AntdCheckCard(
            "演示用模拟接口",
            value="演示用模拟接口",
            className="chat-setting-model-card",
        ),
        fac.AntdDivider(isDashed=True),
    ]

    for model in ModelsConfig.models:
        # 当api_key参数不为空时
        if model.get("api_key"):
            children.append(
                fac.AntdSpace(
                    [
                        html.Img(
                            src=model["logo"],
                            width=36,
                        ),
                        fac.AntdText(model["name"], style={"fontSize": 18}),
                    ],
                    align="center",
                ),
            )

            children.extend(
                [
                    fac.AntdSpace(
                        [
                            fac.AntdCheckCard(
                                sub_model["name"],
                                value="%s|%s"
                                % (
                                    model["name"],
                                    sub_model["name"],
                                ),  # 记录模型厂商+模型名称信息
                                className="chat-setting-model-card",
                            )
                            for sub_model in model["sub_models"]
                        ],
                        wrap=True,
                    ),
                    fac.AntdDivider(isDashed=True),
                ]
            )

    return children


def setting_modal():
    """渲染设置中心模态框"""

    return fac.AntdModal(
        html.Div(
            fac.AntdTabs(
                items=[
                    {
                        "label": "模型选择",
                        "key": "模型选择",
                        "forceRender": True,
                        "children": fac.AntdSpace(
                            [
                                fac.AntdAlert(
                                    type="warning",
                                    showIcon=True,
                                    message="切换模型后，当前已有对话记录将重置。",
                                ),
                                fac.AntdCheckCardGroup(
                                    fac.AntdSpace(
                                        models_check_cards(),
                                        direction="vertical",
                                        style={"width": "100%"},
                                    ),
                                    id="chat-setting-model",
                                    className="chat-setting-model-card-group",
                                    value="演示用模拟接口",
                                    allowNoValue=False,
                                ),
                            ],
                            direction="vertical",
                            style={"width": "100%"},
                        ),
                    },
                    {
                        "label": "模型参数",
                        "key": "模型参数",
                        "forceRender": True,
                        "children": fac.AntdForm(
                            [
                                fac.AntdFormItem(
                                    fac.AntdSlider(
                                        id="chat-setting-temperature",
                                        value=0.5,
                                        min=0,
                                        max=1,
                                        step=0.1,
                                        marks={
                                            round(0.1 * i, 1): f"{round(0.1 * i, 1):g}"
                                            for i in range(11)
                                        },
                                        style={"width": "100%"},
                                    ),
                                    label="随机性 (temperature)",
                                    help="值越大，回复越随机",
                                ),
                                fac.AntdFormItem(
                                    fac.AntdInputNumber(
                                        id="chat-setting-max-tokens",
                                        value=4000,
                                        min=1,
                                        step=1,
                                        style={"width": "100%"},
                                    ),
                                    label="单次回复限制 (max_tokens)",
                                    help="单次交互所使用的最大token数",
                                ),
                            ],
                            layout="vertical",
                            style={"paddingRight": 12},
                        ),
                    },
                ],
                tabPosition="left",
                size="large",
                style={"height": "100%"},
            ),
            className="chat-setting-container",
            style={
                "height": "calc(100vh - 400px)",
                "overflowY": "auto",
                "paddingTop": 1,
            },
        ),
        id="chat-setting-modal",
        title=fac.AntdSpace(
            [
                fac.AntdText("设置中心", strong=True, style={"fontSize": 20}),
                fac.AntdText(
                    "所有设置选项，变更后立即生效",
                    style={"fontWeight": "normal", "fontSize": 14},
                ),
            ],
            direction="vertical",
            size=0,
        ),
        width="calc(min(90vw, 1200px))",
        centered=True,
        destroyOnClose=False,
        className={
            "& .ant-modal-content": {"padding": 0},
            "& .ant-modal-header": {
                "padding": "14px 20px",
                "borderBottom": "1px solid #e5e5e5",
                "marginBottom": 0,
            },
        },
    )
