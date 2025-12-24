
/**
 * time: 2025-04-01
 * author: XJ
 * description: 用于实验申请静态配置设置
 */
interface EXPERIMENT_APPLICATION_CONFIG_TYPE {
    table_column: { title: string; dataIndex: string; width: any; render?: any; }[];
    modal_init: {
        visible: false,
        title: "",
        type: null
    }
    validFlagEnum:any
    injectModeEnum:any
}
const EXPERIMENT_APPLICATION_CONFIG: EXPERIMENT_APPLICATION_CONFIG_TYPE = {
    validFlagEnum:{
        1:"新建",
        2:"已提交",
        3:"规划中",
        4:"已规划",
        5:"被拒绝",
        6:"已固定",
        7:"已开始",
        8:"已取消",
        9:"已结束",
        10:"异常"
    },
    injectModeEnum:{
        1:"常规实验",
        2:"遥科学实验",
        3:"立即实验"
    },
    table_column: [
        {
            title: '序号',
            dataIndex: 'index',
            width: 50,
            render: (text: any, record: any, index: number) => index + 1, // 从1开始
        },
        { title: '实验名称', dataIndex: 'expName', width: 176 },
        { title: '计划申请类别', dataIndex: 'planType', width: 176 },
        { title: '子系统', dataIndex: 'levelCode', width: 176 },
        { title: '实验状态', dataIndex: 'validFlag', width: 176 },
        { title: '计划预计开始时间', dataIndex: 'expBegTime', width: 176 },
        { title: '载荷', dataIndex: 'actionName', width: 176 },
        { title: '状态', dataIndex: 'validFlag', width: 176 ,render: (text: any, record: any, index: number) => EXPERIMENT_APPLICATION_CONFIG.validFlagEnum[record["validFlag"]]},
        { title: '实验方式', dataIndex: 'injectMode', width: 176,render: (text: any, record: any, index: number) => EXPERIMENT_APPLICATION_CONFIG.injectModeEnum[record["injectMode"]] },
    ],
    modal_init: {
        visible: false,
        title: "",
        type: null
    }
}
export default EXPERIMENT_APPLICATION_CONFIG;