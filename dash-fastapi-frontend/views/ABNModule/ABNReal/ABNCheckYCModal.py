import feffery_antd_components as fac
from dash import dcc, html


def render_check_YC_modal():
    return [
        fac.AntdSpin(
            fac.AntdModal(
                [
                    # fac.AntdRow(
                    #     [
                    #         fac.AntdCol(
                    #             fac.AntdFormItem(
                    #                 fac.AntdTreeSelect(
                    #                     id='menu-parent_id',
                    #                     placeholder='请选择上级菜单',
                    #                     treeData=[],
                    #                     defaultValue='0',
                    #                     treeNodeFilterProp='title',
                    #                     style={'width': '100%'},
                    #                 ),
                    #                 label='上级菜单',
                    #                 required=True,
                    #                 id='menu-parent_id-form-item',
                    #                 labelCol={'span': 4},
                    #                 wrapperCol={'span': 20},
                    #             ),
                    #             span=24,
                    #         ),
                    #     ],
                    #     gutter=10,
                    # ),
                ],
                id='menu-modal',
                mask=True,
                width="70%",
                renderFooter=True,
                okClickClose=False,
            )
        )
    ]
