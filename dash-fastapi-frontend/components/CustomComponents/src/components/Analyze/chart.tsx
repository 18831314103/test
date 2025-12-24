
/**
 * time: 2025-03-27
 * author: XJ
 * description: 用于统计分析过滤条件筛选
 */

import { Col, Flex, Row, Space } from "antd";
import * as echarts from 'echarts';
import { useEffect } from "react";
import ANALYZE_STATIC_CONFIG from "./staticConfig";

const AnalyzeChart: React.FC = () => {

    useEffect(() => {
        let chartDom_line = document.getElementById('chart_left');
        let myChart_line = echarts.init(chartDom_line);
        let option_line = ANALYZE_STATIC_CONFIG.line_chart_option;
        option_line && myChart_line.setOption(option_line);

        let chartDom_hot = document.getElementById('chart_right');
        let myChart_hot = echarts.init(chartDom_hot);
        let option_hot = ANALYZE_STATIC_CONFIG.hot_chart_option;
        option_hot && myChart_hot.setOption(option_hot);
    }, [])

    return (
        <Flex gap={10} style={{ marginBottom: 10 }}>
            <div style={{ backgroundColor: "#0c0c0c", height: 200, width: "40%",padding:10 }} id="chart_left"></div>
            <div style={{ backgroundColor: "#0c0c0c", height: 200, width: "60%",padding:10 }} id="chart_right"></div>
        </Flex >
    )
}

export default AnalyzeChart;