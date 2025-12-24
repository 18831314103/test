/**
 * time: 2025-04-02
 * author: XJ
 * description: 用于统计分析公用模态框
 */
import React from 'react';
import { useModel } from '@umijs/max';
import 'react-resizable/css/styles.css';
import DraggableModal from '../CommonComp/DraggableResizableModal';
import ANALYZE_STATIC_CONFIG from './staticConfig';
import BaseTable from '../CommonComp/BaseTable';

const initTableWidth = 730
const AnalyzeModal: React.FC = () => {
    const { analyzeModal, setAnalyzeModal } = useModel("Analyze.modalState");

    const modalFinish = () => {
        setAnalyzeModal(item => ({ ...ANALYZE_STATIC_CONFIG.modal_init }))
    }
    return (
        <>
            <DraggableModal
                title={analyzeModal.title}
                open={analyzeModal.visible}
                onOk={() => modalFinish()}
                onCancel={() => setAnalyzeModal(item => ({ ...ANALYZE_STATIC_CONFIG.modal_init }))}
                width={window.innerWidth * 0.8}
                height={window.innerHeight * 0.4}
                footer={null}
                loading={analyzeModal.loading}
            >
                <BaseTable
                    tableWidth={initTableWidth}
                    columnsA={[
                        // { key: 'sort', align: 'center', width: 40, render: () => <DragHandle /> },
                        ...ANALYZE_STATIC_CONFIG.modal_table_column,

                    ].map((col, index) => ({
                        ...col,
                        width: index == 0 ? col.width : (initTableWidth - 87) / ANALYZE_STATIC_CONFIG.modal_table_column.length - 1,
                        onHeaderCell: () => ({
                            width: index == 0 ? col.width : (initTableWidth - 87) / ANALYZE_STATIC_CONFIG.modal_table_column.length - 1,
                            index
                        }),
                    }))}
                    pagination={false}
                    table_state={{ dataSource: analyzeModal.data, isCollapsible: false }}
                    table_state_fun={() => { }}
                    twoHeight={[window.innerHeight * (1 - 0.4) + 98, window.innerHeight * (1 - 0.4) + 98]}
                />
            </DraggableModal>
        </>
    );
};

export default AnalyzeModal;