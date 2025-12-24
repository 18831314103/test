/**
 * time: 2025-06-05
 * author: XJ
 * description: 数据管理头部信息
 */
import React from 'react';
import { Form, Input, Select, Button, message, Row, Upload, UploadProps } from 'antd';

const { Option } = Select;
const uploadProps: UploadProps = {
  name: 'file',
  action: 'http://localhost:8000/api/xml/parse-folder',
  accept: '.xml, application/xml', // 仅允许 XML 文件
  showUploadList: false,
  multiple: true,
  directory: true,
  onChange(info) {
    if (info.file.status !== 'uploading') {
      console.log(info.file, info.fileList);
    }
    if (info.file.status === 'done') {
      message.success(`${info.file.name} file uploaded successfully`);
    } else if (info.file.status === 'error') {
      message.error(`${info.file.name} file upload failed.`);
    }
  },
};
const DataManagerHeader: React.FC = () => {
  const [form] = Form.useForm();

  const beforeUpload = (file: { name: string }) => {
    const isXml = file.name.endsWith('.xml') || file.name.endsWith('.XML');

    if (!isXml) {
      message.warning(`${file.name} 不是 XML 文件，已跳过`);
    }

    return isXml || Upload.LIST_IGNORE; // 忽略非 XML 文件
  };
  const handleFinish = (values: any) => {
    console.log('提交数据:', values);
    // 你可以在这里调用接口，例如 axios.post('/api/xxx', values)
    message.success('提交成功');
  };

  return (
    <Row
      gutter={10}
      style={{
        backgroundColor: '#0c0c0c',
        boxSizing: 'border-box',
        marginLeft: 0,
        marginRight: 0,
        padding: 10,
        paddingTop: 20,
        marginBottom: 10,
        borderRadius: '8px 8px 0px 0px',
      }}
    >
      <Form
        form={form}
        name="DataManagerHeaderForm"
        // layout="vertical"
        onFinish={handleFinish}
        style={{ width: '100%' }}
      >
        <Form.Item label="姓名" name="name" rules={[{ required: true, message: '请输入姓名' }]}>
          <Input placeholder="请输入姓名" />
        </Form.Item>

        <Form.Item>
          <Button htmlType="submit">
            提交
          </Button>
          <Button style={{ marginLeft: 12 }} onClick={() => form.resetFields()}>
            重置
          </Button>
          <Upload  {...uploadProps} beforeUpload={beforeUpload}>
            <Button  style={{ marginLeft: 12 }}>上传</Button>
          </Upload>
        </Form.Item>
      </Form>
    </Row>
  );
};

export default DataManagerHeader;
