import dash
from dash import html
import feffery_antd_components as fac
from feffery_dash_utils.style_utils import style
from dash.dependencies import Input, Output, ClientsideFunction

app = dash.Dash(
    __name__,
    external_scripts=[
        "https://unpkg.com/@univerjs/umd/lib/univer.full.umd.js",
        "https://unpkg.com/@univerjs/umd/lib/locale/zh-CN.js",
    ],
    external_stylesheets=["https://unpkg.com/@univerjs/umd/lib/univer.css"],
)

app.layout = html.Div(
    fac.AntdSpace(
        [
            fac.AntdTitle("电子表格基础示例：", level=4),
            html.Div(id="univer-container", style=style(height=800)),
        ],
        direction="vertical",
        style=style(width="100%"),
    ),
    style=style(padding=8),
)


app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="renderUniver"),
    Output("univer-container", "children"),
    Input("univer-container", "id"),
)

if __name__ == "__main__":
    app.run(debug=True,port=8055)
