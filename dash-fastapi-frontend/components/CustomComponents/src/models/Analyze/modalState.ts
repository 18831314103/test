/**
 * Author: XJ
 * Date: 2025-04-03
 * Description: 用于数据分析Modal模块Model层
 * */
import { useState, useCallback, SetStateAction } from "react";

const initData: {
    visible: boolean
    title: string
    loading: boolean
    data: any
} = {
    visible: false,
    title: "",
    loading: false,
    data: []
};
export default function dialogStatus() {
    const [analyzeModal, setAnalyzeModal] = useState(initData);
    return {
        analyzeModal,
        setAnalyzeModal
    }
}