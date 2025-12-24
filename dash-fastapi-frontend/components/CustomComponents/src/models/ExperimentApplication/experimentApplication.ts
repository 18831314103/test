/**
 * Author: XJ
 * Date: 2025-04-01
 * Description: 用于实验申请Model层
 * */
import { useState, useCallback, SetStateAction } from "react";

const initData: {
    dataSource: any[];
    filters: { [key: string]: any };
    isCollapsible: boolean;
    selectRowKeys: React.Key[]
    total: number;
    current: number;
    pageSize: number;
} = {
    dataSource: [{
        a: "",
        key:"a"
    }],
    filters: [],
    total: 0,
    current: 1,
    pageSize: 10,
    isCollapsible: false,
    selectRowKeys:[]
};
export default function dialogStatus() {
    const [experimentApplicationProps, setExperimentApplicationProps] = useState(initData);
    return {
        experimentApplicationProps,
        setExperimentApplicationProps
    }
}