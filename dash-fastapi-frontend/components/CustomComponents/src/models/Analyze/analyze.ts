/**
 * Author: XJ
 * Date: 2025-03-27
 * Description: 用于统计分析Model层
 * */
import { useState, useCallback, SetStateAction } from "react";

const initData: {
    experimentNames: { id: string; name: string }[];
    dataSource: any[];
    filters: { [key: string]: any };
    isCollapsible: boolean;
    total: number;
    current: number;
    pageSize: number;
} = {
    experimentNames: [],
    dataSource: [{
        a: "",
    }],
    filters: {},
    total: 0,
    current: 1,
    pageSize: 10,
    isCollapsible: false
};
export default function dialogStatus() {
    const [analyzeProps, setAnalyzeProps] = useState(initData);
    return {
        analyzeProps,
        setAnalyzeProps
    }
}