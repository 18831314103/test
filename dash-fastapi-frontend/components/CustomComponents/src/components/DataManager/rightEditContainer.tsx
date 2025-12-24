import React, { useEffect, useState } from 'react';
import { Form, Input, Button, Table, Popconfirm, message, Select, Row, Col } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import { useModel } from '@umijs/max';
import keyForTable from './keyForTable';

const { Option } = Select;

const RightEditContainer: React.FC = () => {
  const [form] = Form.useForm();
  const { paramSource } = useModel('DataManager.paramSource');
  const [parameters, setParameters] = useState<any[]>([]);
  const [changeArray, setChangeArray] = useState<{ [key: string]: { [key: string]: any } }>({
    OIM_EXPERIMENT_ACTION_TEMPLATE: {},
    OIM_EXPERIMENT_PARA_TEMPLATE: {},
    OIM_EXPERIMENT_PARA_RANGE: {},
    OIM_EXPERIMENT_PARAVALUE_TEMPL: {},
  });
  // 初始化
  useEffect(() => {
    const listWithSelection = paramSource.tableSource.map((item) => ({
      ...item,
      paraCode: item.optionalValues,
      optionalValues: item.valueList
        ? item.optionalValues
        : `[${item.range.minValue},${item.range.maxValue}]`,
      paraDesc: item.valueList
        ? item.valueList.find((v: { paraCode: any }) => v.paraCode === item.optionalValues)
            ?.paraDesc || ''
        : item.range.paraDesc,
    }));
    setParameters(listWithSelection);
    form.setFieldsValue({ parameters: listWithSelection, actionProps: paramSource.actionData });
  }, [paramSource]);

  const handleSelectChange = (value: string, _option: any, index: number) => {
    const newParams = [...parameters];
    const selected = newParams[index];
    const matched = selected.valueList.find((v: any) => v.paraCode === value);
    selected.optionalValues = value;
    selected.paraCode = matched?.paraCode || '';
    selected.paraDesc = matched?.paraDesc || '';
    newParams[index] = { ...selected };

    setParameters(newParams);
    form.setFieldsValue({ parameters: newParams });
  };

  const handleAdd = () => {
    const newParams = [
      ...parameters,
      {
        parameterName: '',
        optionalValues: '',
        paraCode: '',
        paraDesc: '',
        valueList: [],
      },
    ];
    setParameters(newParams);
    form.setFieldsValue({ parameters: newParams });
  };

  const handleRemove = (index: number) => {
    const newParams = parameters.filter((_, i) => i !== index);
    setParameters(newParams);
    form.setFieldsValue({ parameters: newParams });
  };

  const onFinish = (values: any) => {
    console.log(changeArray);
    console.log('提交参数:', values);
    message.success('提交成功');
  };

  const columns = [
    {
      title: '参数名',
      render: (_: any, __: any, index: number) => (
        <Form.Item
          name={['parameters', index, 'parameterName']}
          rules={[
            {
              required: true,
              message: '参数名为必填项！',
            },
          ]}
        >
          <Input placeholder="请输入参数值" allowClear />
        </Form.Item>
      ),
    },
    {
      title: '参数值/范围',
      render: (_: any, __: any, index: number) => {
        if (parameters[index]?.parameterType == '范围') {
          return (
            <Form.Item
              name={['parameters', index, 'optionalValues']}
              rules={[
                {
                  required: true,
                  message: `范围最大值为${parameters[index].range.maxValue},最小值为${parameters[index].range.minValue}`,
                },
                {
                  validator: (rule: any, value: any = '', callback: Function) => {
                    const newValue = value.replaceAll(' ', '');
                    if (newValue == '') return Promise.reject();
                    const regexValue = /^[\[\(]([0-9a-fA-F]{1,}),([0-9a-fA-F]{1,})[\]\)]$/;
                    if (!regexValue.test(newValue)) {
                      return Promise.reject('请输入十六进制范围');
                    }
                    return Promise.resolve();
                  },
                },
              ]}
            >
              <Input
                addonBefore={`[${parameters[index].range.minValue},${parameters[index].range.maxValue}]`}
                placeholder={`请输入范围值`}
              />
            </Form.Item>
          );
        } else {
          return (
            <Form.Item name={['parameters', index, 'optionalValues']} rules={[{ required: true }]}>
              <Select
                // onChange={(value, option) => handleSelectChange(value, option, index)}
                placeholder="请选择"
              >
                {(parameters[index]?.valueList || []).map((item: any) => (
                  <Option key={item.paraCode} value={item.paraCode}>
                    {item.paraDesc}
                  </Option>
                ))}
              </Select>
            </Form.Item>
          );
        }
      },
    },
    {
      title: '码值',
      render: (_: any, __: any, index: number) => (
        <Form.Item name={['parameters', index, 'paraCode']}>
          <Input disabled={parameters[index]?.parameterType == '范围'} />
        </Form.Item>
      ),
    },
    {
      title: '物理意义',
      render: (_: any, __: any, index: number) => (
        <Form.Item name={['parameters', index, 'paraDesc']}>
          <Input />
        </Form.Item>
      ),
    },
    {
      title: '操作',
      render: (_: any, __: any, index: number) => (
        <Popconfirm title="确认删除该参数？" onConfirm={() => handleRemove(index)}>
          <a>删除</a>
        </Popconfirm>
      ),
    },
  ];
  const formOnChange = (changedValues: any) => {
    if ('parameters' in changedValues) {
      for (let i = 0; i < changedValues.parameters.length; i++) {
        if (changedValues.parameters[i]) {
          const originDataItem = paramSource.tableSource[i];
          const tableKey = Object.keys(changedValues.parameters[i])[0];
          if (originDataItem.parameterType == '范围') {
          } else {
            if (tableKey == 'optionalValues') {
              form.setFieldValue(
                ['parameters', i, 'paraCode'],
                changedValues.parameters[i][tableKey],
              );
            }
            if(tableKey == 'paraCode'){
              const parametersList = form.getFieldValue('parameters');
              const nowSelectOptionIndex = parametersList[i].valueList.findIndex(
                (item: { paraCode: any }, index: number) => {
                  return item.paraCode == parametersList[i].optionalValues;
                },
              );
              setParameters((item) => {
                  const newItem = JSON.parse(JSON.stringify(item));
                  newItem[i].optionalValues = changedValues.parameters[i][tableKey];
                  newItem[i].valueList[nowSelectOptionIndex].paraCode =
                    changedValues.parameters[i][tableKey];
                  return newItem;
                });
            }
          }



          // if (keyForTable.OIM_EXPERIMENT_PARA_TEMPLATE.includes(tableKey)) {
          //   if (tableKey == 'optionalValues' && originDataItem.parameterType == '范围') {
          //     const regexValue = /^[\[\(]([0-9a-fA-F]{1,}),([0-9a-fA-F]{1,})[\]\)]$/;
          //     if (!regexValue.test(changedValues.parameters[i][tableKey])) {
          //       break;
          //     }
          //   }
          //   setChangeArray((changeArrayItem) => {
          //     const obj = changeArrayItem['OIM_EXPERIMENT_PARA_TEMPLATE'];
          //     obj[originDataItem.parameterTemplateId] = obj[originDataItem.parameterTemplateId]
          //       ? {
          //           ...obj[originDataItem.parameterTemplateId],
          //           [tableKey]: changedValues.parameters[i][tableKey],
          //         }
          //       : { [tableKey]: changedValues.parameters[i][tableKey] };
          //     if (obj[originDataItem.parameterTemplateId][tableKey] == originDataItem[tableKey]) {
          //       delete obj[originDataItem.parameterTemplateId][tableKey];
          //     }
          //     if (tableKey == 'optionalValues') {
          //       if (originDataItem.parameterType == '范围') {
          //         const objRange = changeArrayItem['OIM_EXPERIMENT_PARA_RANGE'];
          //         const rangeList = changedValues.parameters[i][tableKey]
          //           .replaceAll(/\[\]\(\)/g, '')
          //           .split(',');
          //         objRange[originDataItem.range.parameterRangeId] = objRange[
          //           originDataItem.range.parameterRangeId
          //         ]
          //           ? {
          //               ...objRange[originDataItem.range.parameterRangeId],
          //               minValue: rangeList[0],
          //               maxValue: rangeList[1],
          //             }
          //           : {
          //               minValue: rangeList[0],
          //               maxValue: rangeList[1],
          //             };
          //         if (
          //           objRange[originDataItem.range.parameterRangeId].minValue ==
          //           originDataItem.range.minValue
          //         ) {
          //           delete objRange[originDataItem.range.parameterRangeId].minValue;
          //         }
          //         if (
          //           objRange[originDataItem.range.parameterRangeId].maxValue ==
          //           originDataItem.range.maxValue
          //         ) {
          //           delete objRange[originDataItem.range.parameterRangeId].maxValue;
          //         }
          //       } else {
          //         form.setFieldValue(
          //           ['parameters', i, 'paraCode'],
          //           changedValues.parameters[i][tableKey],
          //         );
          //       }
          //     }
          //     return changeArrayItem;
          //   });
          //   break;
          // }

          // if (
          //   keyForTable.OIM_EXPERIMENT_PARA_RANGE.includes(tableKey) &&
          //   originDataItem.parameterType == '范围'
          // ) {
          //   setChangeArray((changeArrayItem) => {
          //     const objRange = changeArrayItem['OIM_EXPERIMENT_PARA_RANGE'];

          //     objRange[originDataItem.range.parameterRangeId] = objRange[
          //       originDataItem.range.parameterRangeId
          //     ]
          //       ? {
          //           ...objRange[originDataItem.range.parameterRangeId],
          //           [tableKey]: changedValues.parameters[i][tableKey],
          //         }
          //       : {
          //           [tableKey]: changedValues.parameters[i][tableKey],
          //         };
          //     if (
          //       objRange[originDataItem.range.parameterRangeId][tableKey] ==
          //       originDataItem.range[tableKey]
          //     ) {
          //       delete objRange[originDataItem.range.parameterRangeId][tableKey];
          //     }
          //     return changeArrayItem;
          //   });
          //   break;
          // }

          // if (keyForTable.OIM_EXPERIMENT_PARAVALUE_TEMPL.includes(tableKey)) {
          //   setChangeArray((changeArrayItem) => {
          //     const objValue = changeArrayItem['OIM_EXPERIMENT_PARAVALUE_TEMPL'];
          //     const parametersList = form.getFieldValue('parameters');
          //     const nowSelectOptionIndex = parametersList[i].valueList.findIndex(
          //       (item: { paraCode: any }, index: number) => {
          //         return item.paraCode == parametersList[i].optionalValues;
          //       },
          //     );
          //     const nowSelectOption = parametersList[i].valueList[nowSelectOptionIndex];
          //     objValue[nowSelectOption.paravalueTemplateId] = objValue[
          //       nowSelectOption.paravalueTemplateId
          //     ]
          //       ? {
          //           ...objValue[nowSelectOption.paravalueTemplateId],
          //           [tableKey]: changedValues.parameters[i][tableKey],
          //         }
          //       : {
          //           [tableKey]: changedValues.parameters[i][tableKey],
          //         };
          //     if (
          //       objValue[nowSelectOption.paravalueTemplateId][tableKey] ==
          //       originDataItem.valueList[nowSelectOptionIndex][tableKey]
          //     ) {
          //       delete objValue[nowSelectOptionIndex][tableKey];
          //     }
          //     if (tableKey == 'paraCode') {
          //       // parametersList[i].optionalValues = changedValues.parameters[i][tableKey];
          //       const obj = changeArrayItem['OIM_EXPERIMENT_PARA_TEMPLATE'];
          //       obj[originDataItem.parameterTemplateId] = obj[originDataItem.parameterTemplateId]
          //         ? {
          //             ...obj[originDataItem.parameterTemplateId],
          //             [tableKey]: changedValues.parameters[i][tableKey],
          //           }
          //         : { [tableKey]: changedValues.parameters[i][tableKey] };
          //       if (obj[originDataItem.parameterTemplateId][tableKey] == originDataItem[tableKey]) {
          //         delete obj[originDataItem.parameterTemplateId][tableKey];
          //       }
          //       setParameters((item) => {
          //         const newItem = JSON.parse(JSON.stringify(item));
          //         newItem[i].optionalValues = changedValues.parameters[i][tableKey];
          //         newItem[i].valueList[nowSelectOptionIndex].paraCode =
          //           changedValues.parameters[i][tableKey];
          //         return newItem;
          //       });
          //       // form.setFieldsValue({ parameters: parametersList });
          //     }
          //     return changeArrayItem;
          //   });
          //   break;
          // }
        }
      }
    }
  };
  return (
    <div
      style={{
        backgroundColor: '#0c0c0c',
        padding: 10,
        position: 'relative',
        width: '100%',
        minWidth: '800px',
      }}
    >
      <Form onValuesChange={formOnChange} form={form} onFinish={onFinish}>
        <Row gutter={10}>
          <Col span={12}>
            <Form.Item
              label="事件名称"
              name={['actionProps', 'action', 'actionName']}
              rules={[{ required: true, message: '事件名称不可为空!' }]}
            >
              <Input allowClear placeholder="请输入事件名称" />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="事件类型"
              name={['actionProps', 'action', 'type']}
              rules={[{ required: true, message: '事件类型不可为空!' }]}
            >
              <Select
                placeholder="请选择事件类型"
                allowClear
                showSearch
                options={[
                  { value: 0, label: '数据注入' },
                  { value: 1, label: '平台B令(总线令)' },
                  { value: 2, label: '平台P令(程控指令)' },
                  { value: 3, label: '非结构文件事件' },
                  { value: 4, label: '结构文件事件' },
                ]}
              />
            </Form.Item>
          </Col>
        </Row>
        <Table
          pagination={false}
          dataSource={parameters}
          columns={columns}
          rowKey={(_, index) => index!.toString()}
          size="small"
          // footer={() => (
          //   <Button type="dashed" icon={<PlusOutlined />} onClick={handleAdd} block>
          //     添加参数
          //   </Button>
          // )}
        />
        <Form.Item style={{ marginTop: 24 }}>
          <Button type="primary" htmlType="submit">
            提交
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export default RightEditContainer;
