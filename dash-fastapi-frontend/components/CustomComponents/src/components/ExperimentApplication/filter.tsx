
/**
 * time: 2025-04-01
 * author: XJ
 * description: 用于实验申请过滤条件筛选
 */
import { getExpListAPI } from "@/services/apis/analyze";
import { useModel } from "@umijs/max";
import { Col, Form, Input, Row, Select, DatePicker, Button, Space } from "antd"
import { useEffect } from "react";
import DraggableResizableModal from "../CommonComp/DraggableResizableModal";
import DraggableModal from "../CommonComp/DraggableResizableModal";
import { selectExpChild } from "@/services/apis/experiment";

const { RangePicker } = DatePicker;
const formItemLayout = {
    labelCol: {
        span: 6
    },

};
const ExperimentApplicationFilter: React.FC = () => {
    const { experimentApplicationProps, setExperimentApplicationProps } = useModel("ExperimentApplication.experimentApplication");
    const { experimentModal, setExperimentModal } = useModel("ExperimentApplication.modalState");

    const getTableData = () => {

    }

    const selectExpChildFun = (pageSize: number, pageNo: number, values: any) => {
        selectExpChild({}).then(res => {
            const { success, data, msg } = res;
            if (success) {
                setExperimentApplicationProps(item => ({ ...item, dataSource: data, filters: values, total: 100 }))
            }
        })
    }

    useEffect(() => {
        selectExpChildFun(experimentApplicationProps.pageSize, experimentApplicationProps.current, experimentApplicationProps.filters);
    }, [experimentApplicationProps.current, experimentApplicationProps.pageSize])
    const showExperimentModal = () => {
        setExperimentModal({ ...experimentModal, title: "申请实验", visible: true, type: "expriment" })
    }
    return (
        <>
            <Row
                gutter={10}
                style={{
                    backgroundColor: "#0c0c0c",
                    boxSizing: "border-box",
                    marginLeft: 0,
                    marginRight: 0,
                    padding: 10,
                    paddingTop: 20,
                    marginBottom: 10,
                    borderRadius: "8px 8px 0px 0px"
                }}
            >
                <Form
                    name="data_manager_filter"
                    style={{ maxWidth: "100%", display: "contents" }}
                    initialValues={{ remember: true }}
                    onFinish={(values) => selectExpChildFun(experimentApplicationProps.pageSize, experimentApplicationProps.current, values)}
                    // onFinishFailed={onFinishFailed}
                    size="middle"
                    {...formItemLayout}
                    autoComplete="off"
                >
                    <Col span={5}>
                        <Form.Item
                            label="实验状态"
                            name="validFlag"
                        >
                            <Select
                                options={[
                                    {
                                        value: 1,
                                        label: '新建',
                                    },
                                    { label: '已提交', value: 2 },
                                    { label: '规划中', value: 3 },
                                    { label: '已规划', value: 4 },
                                    {
                                        value: 5,
                                        label: '被拒绝',
                                    },
                                    { label: '已固定', value: 6 },
                                    { label: '已开始', value: 7 },
                                    { label: '已结束', value: 9 },
                                    { label: '异常', value: 10 },
                                ]}
                                placeholder="请选择实验状态"
                            />
                        </Form.Item>
                    </Col>
                    <Col span={7}>
                        <Form.Item
                            label="子系统"
                            name="levelCode"
                        >
                            <Select
                                options={[
                                    { label: "光学舱", value: "TGXT" }
                                ]}
                                placeholder="请选所属子系统"
                            />
                        </Form.Item>
                    </Col>
                    <Col span={12}>
                        <Form.Item
                            label="计划预计开始时间"
                            name="begTime_begin"
                        >
                            <RangePicker
                                showTime={{ format: 'HH:mm' }}
                                format="YYYY-MM-DD HH:mm"
                                onChange={(value, dateString) => {
                                    console.log('Selected Time: ', value);
                                    console.log('Formatted Selected Time: ', dateString);
                                }}
                            />
                        </Form.Item>
                    </Col>

                    <Col span={5}>
                        <Form.Item
                            label="实验名称"
                            name="expName"
                        >
                            <Input placeholder="请输入实验名称" />
                        </Form.Item>
                    </Col>
                    <Col span={7}>
                        <Form.Item
                            label="计划申请类别"
                            name="planType"
                        >
                            <Select
                                options={[
                                    {
                                        value: '1',
                                        label: '科学实验申请',
                                    },
                                    { label: '维修更换申请', value: '2' },
                                    { label: '对地遥感申请', value: '15' },
                                    { label: '天文观测申请', value: '16' },
                                    { label: '跟踪观测申请', value: '17' },
                                ]}
                                placeholder="请选择计划申请类别"
                            />
                        </Form.Item>
                    </Col>
                    <Col span={24}>
                        <Form.Item label={null} labelCol={{ span: 0 }}>
                            <Space>
                                <Button htmlType="submit">
                                    查询
                                </Button>
                                <Button>
                                    重置
                                </Button>
                                <Button>
                                    批量复制
                                </Button>
                                <Button>
                                    批量删除
                                </Button>
                                <Button onClick={showExperimentModal}>
                                    申请实验
                                </Button>
                            </Space>
                        </Form.Item>
                    </Col>
                </Form>
            </Row>
        </>
    )
}

export default ExperimentApplicationFilter;