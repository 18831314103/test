/**
 * time: 2025-03-27
 * author: XJ
 * description: 用于基本数据管理入口文件
 */

import PageContainerComp from "@/components/CommonComp/pageContainer"
import DataManagerHeader from "@/components/DataManager/header"
import LeftTree from "@/components/DataManager/leftTree"
import RightEditContainer from "@/components/DataManager/rightEditContainer"
import { Col, Row } from "antd"

const DataManager:React.FC = () => {


    return (
        <PageContainerComp>
            <Row 
                gutter={10}
                style={{ height: window.innerHeight - 86, boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)' }}
            >
                <Col span={6}>
                    <DataManagerHeader />
                    <LeftTree />
                </Col>
                <Col span={18}>
                    <RightEditContainer />
                </Col>
            </Row>
        </PageContainerComp>
    )
}

export default DataManager