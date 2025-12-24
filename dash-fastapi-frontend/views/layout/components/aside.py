import feffery_antd_components as fac
from dash import dcc, get_asset_url
from callbacks.layout_c import aside_c  # noqa: F401
from config.env import AppConfig


def render_aside_content(menu_info):
    return [
        dcc.Store(id='current-key_path-store'),
        dcc.Store(id='current-item-store'),
        dcc.Store(id='current-item_path-store'),
        fac.AntdSider(
            [
                fac.AntdRow(
                    [
                        fac.AntdCol(
                            fac.AntdImage(
                                width=50,
                                height=50,
                                src=get_asset_url('imgs/CSU-removebg.png'),
                                preview=False,
                            ),
                            flex='1',
                            style={
                                'height': '100%',
                                'display': 'flex',
                                'alignItems': 'center',
                            },
                        ),
                        fac.AntdCol(
                            fac.AntdText(
                                '空间科学设施健康管理平台V1.0',
                                id='logo-text',
                                style={
                                    'fontSize': '24px',
                                    'color': 'rgb(255, 255, 255)',
                                    'fontFamily': 'title_font',
                                },
                            ),
                            flex='5',
                            style={
                                'height': '100%',
                                'display': 'flex',
                                'alignItems': 'center',
                                'marginLeft': '10px',
                            },
                        ),
                    ],
                    style={
                        'height': '80px',
                        'background': '#1e2229',
                        'position': 'sticky',
                        'top': 0,
                        'zIndex': 999,
                        'paddingLeft': '10px',
                        'paddingTop': '20px',
                    },
                ),
                fac.AntdMenu(
                    id='index-side-menu',
                    menuItems=menu_info,
                    mode='inline',
                    theme='dark',
                    defaultSelectedKey='首页',
                    style={'width': '100%', 'height': 'calc(100vh - 80px)'},
                ),
            ],
            id='menu-collapse-sider-custom',
            collapsible=True,
            collapsedWidth=64,
            trigger=None,
            width=256,
        ),
    ]
