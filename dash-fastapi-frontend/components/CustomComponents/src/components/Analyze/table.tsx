/**
 * time: 2025-03-27
 * author: XJ
 * description: 用于统计分析表格数据展示
 */

import React from 'react';
import { useModel } from '@umijs/max';
import 'react-resizable/css/styles.css';
import ANALYZE_STATIC_CONFIG from './staticConfig';
import BaseTable from '../CommonComp/BaseTable';
import { Button, Space } from 'antd';
import { sendActionParaList } from '@/services/apis/analyze';

const initTableWidth = window.innerWidth - 256 - 30;
const TableCom: React.FC = () => {
    const { analyzeProps, setAnalyzeProps } = useModel("Analyze.analyze");
    const { analyzeModal, setAnalyzeModal } = useModel("Analyze.modalState");

    const pagePropsChange = (page: number, pageSize: number) => {
        setAnalyzeProps({ ...analyzeProps, current: page, pageSize })
    }
    const tableRowAction = (e: React.MouseEvent<HTMLElement>, text: any, record: any, index: number) => {
        const type = (e.target as any).textContent.replaceAll(" ", "");
        switch (type) {
            case "删除":

                break;
            case "详情":
                setAnalyzeModal(item => ({ ...item, visible: true, loading: true, title: "实验详情" }));
                const { actionEditId } = record;
                sendActionParaList({ actionEditId }).then(res => {
                    const { success, data, msg } = res;
                    if (success) {
                        setAnalyzeModal(item => ({ ...item, data, loading: false }))
                    }
                })
                break;
            case "复制":

                break
            default:
                void 0;
        }
    }
    return (
        <div>
            <BaseTable
                tableWidth={initTableWidth}
                columnsA={[
                    // { key: 'sort', align: 'center', width: 40, render: () => <DragHandle /> },
                    ...ANALYZE_STATIC_CONFIG.table_column,
                    {
                        key: 'sort', title: "操作", width: 80, render: (text: any, record: any, index: number) => {

                            return (
                                <Space size={"small"} onClick={(e) => tableRowAction(e, text, record, index)}>
                                    <Button size='small'>详情</Button>
                                    {/* <Button size='small'>查看</Button> */}
                                    {/* <Button size='small'>复制</Button> */}
                                </Space>
                            )
                        }
                    },

                ].map((col, index) => ({
                    ...col,
                    width: index == 0 || index == ANALYZE_STATIC_CONFIG.table_column.length ? col.width : (initTableWidth - 87) / ANALYZE_STATIC_CONFIG.table_column.length - 1,
                    onHeaderCell: () => ({
                        width: index == 0 || index == ANALYZE_STATIC_CONFIG.table_column.length ? col.width : (initTableWidth - 87) / ANALYZE_STATIC_CONFIG.table_column.length - 1,
                        index
                    }),
                }))}
                pagination={{
                    total: analyzeProps.total,
                    current: analyzeProps.current,
                    pageSize: analyzeProps.pageSize,
                    pageSizeOptions: [10, 20, 50],
                    size: "small",
                    onChange: pagePropsChange
                }}
                table_state={analyzeProps}
                table_state_fun={setAnalyzeProps}
                twoHeight={[305, 525]}
            />
        </div>
    );
};

export default TableCom;