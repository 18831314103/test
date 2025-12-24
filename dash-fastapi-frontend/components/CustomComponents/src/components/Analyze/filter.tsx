
/**
 * time: 2025-03-27
 * author: XJ
 * description: 用于统计分析过滤条件筛选
 */
import { getExpListAPI, sendExpList } from "@/services/apis/analyze";
import { useModel } from "@umijs/max";
import { Col, Form, Input, Row, Select, DatePicker, Button } from "antd"
import { useEffect } from "react";
import dayjs from 'dayjs';

const { RangePicker } = DatePicker;
const formItemLayout = {
    labelCol: {
        span: 6
    },

};
const AnalyzeFilter: React.FC = () => {
    const { analyzeProps, setAnalyzeProps } = useModel("Analyze.analyze");

    const getTableData = (pageSize: number, pageNo: number, values: any) => {
        if ("executeTime" in values) {
            values.executeTimeStart = dayjs(values.executeTime[0]).format("YYYY-MM-DD HH:mm:ss.SSS");
            values.executeTimeEnd = dayjs(values.executeTime[1]).format("YYYY-MM-DD HH:mm:ss.SSS");
        }
        if ("submitTime" in values) {
            values.submitTimeStart = dayjs(values.submitTime[0]).format("YYYY-MM-DD HH:mm:ss.SSS");
            values.submitTimeEnd = dayjs(values.submitTime[1]).format("YYYY-MM-DD HH:mm:ss.SSS");
        }
        if ("sendTime" in values) {
            values.sendTimeStart = dayjs(values.sendTime[0]).format("YYYY-MM-DD HH:mm:ss.SSS");
            values.sendTimeEnd = dayjs(values.sendTime[1]).format("YYYY-MM-DD HH:mm:ss.SSS");
        }
        sendExpList({
            ...values,
            pageSize,
            pageNo,
        }).then(res => {
            if (res.success) {
                setAnalyzeProps({ ...analyzeProps, dataSource: res.data.records, filters: values, total: +res.data.total })
            }
        });
    }

    const getExpList = () => {
        getExpListAPI({ pageNo: 1, pageSize: 50 }).then(res => {

        })
    }

    useEffect(() => {
        // getExpList();
        getTableData(analyzeProps.pageSize, analyzeProps.current, analyzeProps.filters);
    }, [analyzeProps.current, analyzeProps.pageSize])

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
                    onFinish={(values) => getTableData(analyzeProps.pageSize, analyzeProps.current, values)}
                    // onFinishFailed={onFinishFailed}
                    size="middle"
                    {...formItemLayout}
                    autoComplete="off"
                >
                    <Col span={6}>
                        <Form.Item
                            label="载荷"
                            name="rackNamePattern"
                        >
                            <Select
                                options={[
                                    { label: "光学舱", value: "TGXT" }
                                ]}
                                placeholder="请选载荷"
                            />
                        </Form.Item>
                    </Col>
                    <Col span={6}>
                        <Form.Item
                            label="子系统"
                            name="subsystemPattern"
                        >
                            <Select
                                options={[
                                    { label: "光学舱", value: "TGXT" }
                                ]}
                                placeholder="请选择舱段"
                            />
                        </Form.Item>
                    </Col>
                    <Col span={12}>
                        <Form.Item
                            label="实验提交时间"
                            name="submitTime"
                        >
                            <RangePicker
                                showTime={{ format: 'HH:mm:ss.SSS' }}
                                format="YYYY-MM-DD HH:mm:ss.SSS"
                            />
                        </Form.Item>
                    </Col>

                    <Col span={6}>
                        <Form.Item
                            label="事件名称"
                            name="actionNamePattern"
                        >
                            <Input placeholder="请输入事件名称" />
                        </Form.Item>
                    </Col>
                    <Col span={6}>
                        <Form.Item
                            label="实验名称"
                            name="expName"
                        >
                            <Select
                                options={[
                                    { label: "光学舱", value: "TGXT" }
                                ]}
                                placeholder="请选择舱段"
                            />
                        </Form.Item>
                    </Col>
                    <Col span={12}>
                        <Form.Item
                            label="执行时间"
                            name="executeTime"
                        >
                            <RangePicker
                                showTime={{ format: 'HH:mm:ss.SSS' }}
                                format="YYYY-MM-DD HH:mm:ss.SSS"
                            />
                        </Form.Item>
                    </Col>
                    <Col span={6}>
                        <Form.Item
                            label="时间类型"
                            name="timeTypePattern"
                        >
                            <Select
                                options={[
                                    { label: "立即令3H", value: "3" },
                                    { label: "延时令6H", value: "6" },
                                    { label: "延时令CH", value: "C" }
                                ]}
                                placeholder="请选时间类型"
                            />
                        </Form.Item>
                    </Col>
                    <Col span={6}>
                        <Form.Item
                            label="传送帧/IP包ID"
                            name="cabinName"
                        >
                            <Select
                                options={[
                                    { label: "光学舱", value: "TGXT" }
                                ]}
                                placeholder="请输入传送帧/IP包ID"
                            />
                        </Form.Item>
                    </Col>
                    <Col span={12}>
                        <Form.Item
                            label="发送时间"
                            name="sendTime"
                        >
                            <RangePicker
                                showTime={{ format: 'HH:mm:ss.SSS' }}
                                format="YYYY-MM-DD HH:mm:ss.SSS"
                            />
                        </Form.Item>
                    </Col>
                    <Col span={2}>
                        <Form.Item label={null} labelCol={{ span: 0 }}>
                            <Button htmlType="submit">
                                查询
                            </Button>
                        </Form.Item>
                    </Col>
                </Form>
            </Row>
        </>
    )
}

export default AnalyzeFilter;