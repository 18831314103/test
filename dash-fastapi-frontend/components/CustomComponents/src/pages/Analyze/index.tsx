/**
 * time: 2025-03-27
 * author: XJ
 * description: 用于统计分析入口文件
 */

import AnalyzeChart from "@/components/Analyze/chart"
import AnalyzeFilter from "@/components/Analyze/filter"
import TableCom from "@/components/Analyze/table"
import PageContainerComp from "@/components/CommonComp/pageContainer"
import { useModel } from "@umijs/max"
import { Splitter } from "antd"
import style from "@/components/Analyze/analyze.module.css";
import AnalyzeModal from "@/components/Analyze/modal"

const Analyze: React.FC = () => {
    const { analyzeProps, setAnalyzeProps } = useModel("Analyze.analyze")
    const onResize = (number:number[]) => {
        if(number[0] == 0){
            setAnalyzeProps({...analyzeProps, isCollapsible:true})
        }else{
            setAnalyzeProps({...analyzeProps, isCollapsible:false})
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
                <Splitter.Panel collapsible resizable={false}  defaultSize={210}>
                    <AnalyzeFilter />
                </Splitter.Panel>
                <Splitter.Panel collapsible resizable={false} style={{overflowY:"hidden"}}>
                    <AnalyzeChart />
                    <TableCom />
                </Splitter.Panel>
            </Splitter>
            <AnalyzeModal />
        </PageContainerComp>
    )
}

export default Analyze