/**
 * time: 2025-03-27
 * author: XJ
 * description: 用于实验申请入口文件
 */

import PageContainerComp from "@/components/CommonComp/pageContainer"
import ExperimentApplicationFilter from "@/components/ExperimentApplication/filter"
import { useModel } from "@umijs/max"
import { Splitter } from "antd"
import style from "@/components/ExperimentApplication/experimentApplication.module.css";
import TableCom from "@/components/ExperimentApplication/table";
import ExperimentModal from "@/components/ExperimentApplication/modal";

const ExperimentApplication: React.FC = () => {

    const { experimentApplicationProps, setExperimentApplicationProps } = useModel("ExperimentApplication.experimentApplication");
    const onResize = (number: number[]) => {
        if (number[0] == 0) {
            setExperimentApplicationProps({ ...experimentApplicationProps, isCollapsible: true })
        } else {
            setExperimentApplicationProps({ ...experimentApplicationProps, isCollapsible: false })
        }
    }
    return (
        <PageContainerComp>
            <Splitter
                rootClassName={style.spliter_css}
                lazy
                layout="vertical"
                style={{ height: window.innerHeight - 86, boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)' }}
                onResize={onResize}
            >
                <Splitter.Panel collapsible resizable={false} defaultSize={166}>
                    <ExperimentApplicationFilter />
                </Splitter.Panel>
                <Splitter.Panel collapsible resizable={false} style={{ overflowY: "hidden" }}>
                    <TableCom />
                </Splitter.Panel>
            </Splitter>
            <ExperimentModal />
        </PageContainerComp>
    )
}
export default ExperimentApplication