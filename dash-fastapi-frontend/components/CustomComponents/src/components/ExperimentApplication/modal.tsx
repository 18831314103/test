/**
 * time: 2025-04-02
 * author: XJ
 * description: 用于实验申请公用模态框
 */
import React from 'react';
import { useModel } from '@umijs/max';
import 'react-resizable/css/styles.css';
import DraggableModal from '../CommonComp/DraggableResizableModal';
import ExperimentCreate from './ExperimentCreate';
import ExperimentDeatil from './ExperimentDeatil';
import EXPERIMENT_APPLICATION_CONFIG from './staticConfig';

const ExperimentModal: React.FC = () => {
    const { experimentApplicationProps, setExperimentApplicationProps } = useModel("ExperimentApplication.experimentApplication");
    const { experimentModal, setExperimentModal } = useModel("ExperimentApplication.modalState");

    const modalFinish = () => {
        setExperimentModal(item => ({ ...EXPERIMENT_APPLICATION_CONFIG.modal_init }))
    }
    return (
        <>
            <DraggableModal
                title={experimentModal.title}
                open={experimentModal.visible}
                onOk={() => modalFinish()}
                onCancel={() => setExperimentModal(item => ({ ...EXPERIMENT_APPLICATION_CONFIG.modal_init }))}
                width={800}
            >
                {
                    experimentModal.type == "expriment" ?
                        (
                            <ExperimentCreate />
                        ) :
                        (
                            <ExperimentDeatil />
                        )
                }
            </DraggableModal>
        </>
    );
};

export default ExperimentModal;