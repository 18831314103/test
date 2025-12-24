/**
 * time: 2025-04-01
 * author: XJ
 * description: 用于实验申请表格数据展示
 */
import React from 'react';
import { Button, Space } from 'antd';
import { useModel } from '@umijs/max';
import 'react-resizable/css/styles.css';
import EXPERIMENT_APPLICATION_CONFIG from './staticConfig';
import BaseTable from '../CommonComp/BaseTable';

const initTableWidth = window.innerWidth - 256 - 30;
const TableCom: React.FC = () => {
    const { experimentApplicationProps, setExperimentApplicationProps } = useModel("ExperimentApplication.experimentApplication");
    const { experimentModal, setExperimentModal } = useModel("ExperimentApplication.modalState");

    const tableRowAction = (e: React.MouseEvent<HTMLElement>, text: any, record: any, index: number) => {
        const type = (e.target as any).textContent.replaceAll(" ", "");
        switch (type) {
            case "删除":

                break;
            case "查看":
                setExperimentModal(item => ({ ...item, visible: true, title: record.expName, type: "detail" }));
                break;
            case "复制":

                break
            default:
                void 0;
        }
    }
    const pagePropsChange = (page: number, pageSize: number) => {
        setExperimentApplicationProps({ ...experimentApplicationProps, current: page, pageSize })
    }
    const selectRowsChange = (selectedRowKeys: React.Key[], selectedRows: any[]) => {
        setExperimentApplicationProps({ ...experimentApplicationProps, selectRowKeys: selectedRowKeys })
    }
    return (
        <>
            <BaseTable
                tableWidth={initTableWidth}
                rowSelection={{
                    type: "checkbox",
                    onChange: selectRowsChange
                }}
                columnsA={[
                    // { key: 'sort', align: 'center', width: 40, render: () => <DragHandle /> },
                    ...EXPERIMENT_APPLICATION_CONFIG.table_column,
                    {
                        key: 'sort', title: "操作", width: 200, render: (text: any, record: any, index: number) => {

                            return (
                                <Space size={5} onClick={(e) => tableRowAction(e, text, record, index)}>
                                    <Button size='small'>删除</Button>
                                    <Button size='small'>查看</Button>
                                    <Button size='small'>复制</Button>
                                </Space>
                            )
                        }
                    },

                ].map((col, index) => ({
                    ...col,
                    width: index == 0 || index == EXPERIMENT_APPLICATION_CONFIG.table_column.length ? col.width : (initTableWidth - 500) / (EXPERIMENT_APPLICATION_CONFIG.table_column.length - 2),
                    onHeaderCell: () => ({
                        width: index == 0 || index == EXPERIMENT_APPLICATION_CONFIG.table_column.length  ? col.width : (initTableWidth - 500) / (EXPERIMENT_APPLICATION_CONFIG.table_column.length - 2),
                        index
                    }),
                }))}
                pagination={{
                    total: experimentApplicationProps.total,
                    current: experimentApplicationProps.current,
                    pageSize: experimentApplicationProps.pageSize,
                    pageSizeOptions: [10, 20, 50],
                    size: "small",
                    onChange: pagePropsChange
                }}
                table_state={experimentApplicationProps}
                table_state_fun={setExperimentApplicationProps}
                twoHeight={[51, 271]}
            />
        </>
    );
};

export default TableCom;