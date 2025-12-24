/**
 * Author: XJ
 * Date: 2025-04-02
 * Description: 用于实验申请Modal模块Model层
 * */
import { useState, useCallback, SetStateAction } from "react";

const initData: {
    visible: boolean
    title: string
    type: "expriment" | "detail" | null
} = {
    visible: false,
    title: "",
    type: null
};
export default function dialogStatus() {
    const [experimentModal, setExperimentModal] = useState(initData);
    return {
        experimentModal,
        setExperimentModal
    }
}