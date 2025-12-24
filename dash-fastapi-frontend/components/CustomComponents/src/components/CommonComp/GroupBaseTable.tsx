import React, { useState } from 'react';
import { Table, Input, Button, Form, Space } from 'antd';
import _ from 'lodash';


const EditableTableForm = () => {
  const [form] = Form.useForm();

  // 添加新表格
  const addTable = () => {
    const tables = form.getFieldValue('tables') || [];
    form.setFieldsValue({
      tables: [...tables, { tableName: `表格${tables.length + 1}`, rows: [{ id: Date.now(), name: '', value: '' }] }]
    });
  };

  // 在指定表格中添加行
  const addRow = (tableIndex) => {
    const tables = [...form.getFieldValue('tables')];
    tables[tableIndex].rows.push({ id: Date.now(), name: '', value: '' });
    form.setFieldsValue({ tables });
  };

  // 处理单元格值变化
  const handleCellChange = (tableIndex, rowIndex, field, value) => {
    const tables = [...form.getFieldValue('tables')];
    tables[tableIndex].rows[rowIndex][field] = value;
    form.setFieldsValue({ tables });
  };

  return (
    <Form form={form} layout="vertical">
      <Form.List name="tables">
        {(fields, { add, remove }) => (
          <>
            {fields.map(({ key, name, ...restField }, tableIndex) => (
              <div key={key} style={{ marginBottom: 16, border: '1px solid #d9d9d9', padding: 16 }}>
                <Form.Item
                  {...restField}
                  name={[name, 'tableName']}
                  label="表格名称"
                  rules={[{ required: true, message: '请输入表格名称' }]}
                >
                  <Input />
                </Form.Item>
                
                <Form.Item shouldUpdate noStyle>
                  {() => (
                    <Table
                      dataSource={form.getFieldValue(['tables', tableIndex, 'rows'])}
                      columns={[
                        {
                          title: '名称',
                          dataIndex: 'name',
                          render: (text, record, rowIndex) => (
                            <Form.Item
                              name={['tables', tableIndex, 'rows', rowIndex, 'name']}
                              rules={[{ required: true, message: '请输入名称' }]}
                              style={{ margin: 0 }}
                            >
                              <Input
                                value={text}
                                onChange={(e) => handleCellChange(tableIndex, rowIndex, 'name', e.target.value)}
                              />
                            </Form.Item>
                          ),
                        },
                        {
                          title: '值',
                          dataIndex: 'value',
                          render: (text, record, rowIndex) => (
                            <Form.Item
                              name={['tables', tableIndex, 'rows', rowIndex, 'value']}
                              rules={[{ required: true, message: '请输入值' }]}
                              style={{ margin: 0 }}
                            >
                              <Input
                                value={text}
                                onChange={(e) => handleCellChange(tableIndex, rowIndex, 'value', e.target.value)}
                              />
                            </Form.Item>
                          ),
                        },
                        {
                          title: '操作',
                          render: (_, __, rowIndex) => (
                            <Button
                              onClick={() => {
                                const tables = [...form.getFieldValue('tables')];
                                tables[tableIndex].rows.splice(rowIndex, 1);
                                form.setFieldsValue({ tables });
                              }}
                            >
                              删除
                            </Button>
                          ),
                        },
                      ]}
                      rowKey="id"
                      pagination={false}
                    />
                  )}
                </Form.Item>
                
                <Button onClick={() => addRow(tableIndex)}>添加行</Button>
                <Button onClick={() => remove(tableIndex)} style={{ marginLeft: 8 }}>删除表格</Button>
              </div>
            ))}
            
            <Button onClick={addTable} type="dashed">添加表格</Button>
          </>
        )}
      </Form.List>
      
      <Form.Item>
        <Button type="primary" onClick={() => console.log(form.getFieldsValue())}>提交</Button>
      </Form.Item>
    </Form>
  );
};

export default EditableTableForm;