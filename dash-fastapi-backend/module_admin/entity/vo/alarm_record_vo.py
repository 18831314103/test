from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic_validation_decorator import Network, NotBlank, Size
from typing import Literal, Optional
from datetime import timedelta


class AlarmRecordModel(BaseModel):
    """
    报警记录对应pydantic模型
    """

    model_config = ConfigDict(from_attributes=True)

    uuid: str = Field(default=None, description='故障模式UUID')
    anomaly_no: str = Field(default=None, description='故障模式编号')
    anomaly_name: str = Field(default=None, description='故障模式名称')
    create_time: datetime = Field(default=None, description='规则创建时间')
    alarm_time: datetime = Field(default=None, description='报警时间')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    data_source: str = Field(default=None, description='数据来源')
    alarm_state: str = Field(default=None, description='报警状态')

    @NotBlank(field_name='uuid', message='模型uuid不能为空')
    @Size(field_name='uuid', min_length=36, max_length=36, message='部门名称长度不能超过36个字符')
    def get_uuid(self):
        return self.uuid

    @NotBlank(field_name='anomaly_no', message='故障模式编号不能为空')
    @Size(field_name='anomaly_no', min_length=1, max_length=50, message='故障模式编号长度不能超过50个字符')
    def get_anomaly_no(self):
        return self.anomaly_no

    @NotBlank(field_name='anomaly_name', message='故障模式名称不能为空')
    @Size(field_name='anomaly_name', min_length=1, max_length=100, message='故障模式名称长度不能超过100个字符')
    def get_anomaly_name(self):
        return self.anomaly_name

    @NotBlank(field_name='create_time', message='规则创建时间不能为空')
    def get_create_time(self):
        return self.create_time

    @NotBlank(field_name='alarm_time', message='报警时间不能为空')
    def get_alarm_time(self):
        return self.alarm_time

    def get_update_time(self):
        return self.update_time

    @NotBlank(field_name='data_source', message='数据来源不能为空')
    @Size(field_name='data_source', min_length=1, max_length=10, message='数据来源长度不能超过50个字符')
    def get_data_source(self):
        return self.data_source

    @NotBlank(field_name='alarm_state', message='报警状态不能为空')
    @Size(field_name='alarm_state', min_length=1, max_length=50, message='报警状态长度不能超过20个字符')
    def get_alarm_state(self):
        return self.alarm_state

    def validate_fields(self):
        self.get_uuid()
        self.get_anomaly_no()
        self.get_anomaly_name()
        self.get_create_time()
        self.get_alarm_time()
        self.get_update_time()
        self.get_data_source()
        self.get_alarm_state()


class AlarmRecordQueryModel(BaseModel):
    """
    报警记录查询模型
    """
    time_delta: int = Field(default=None, description='查询范围')

    @NotBlank(field_name='time_delta', message='查询报警记录范围不能为空')
    def get_time_delta(self):
        return self.time_delta

    def validate_fields(self):
        self.get_time_delta()


class RecentAlarmRecordQueryModel(BaseModel):
    """
    查询最近报警记录查询模型
    """
    anomaly_no: str = Field(..., description="故障编号")
    anomaly_name: str = Field(..., description="故障名称")
    limit: int = Field(..., ge=1, description="要获取的记录条数，最小值为1")

    @NotBlank(field_name='anomaly_no', message='查询故障编号不能为空')
    def get_anomaly_no(self):
        return self.anomaly_no

    @NotBlank(field_name='anomaly_name', message='查询故障名称不能为空')
    def get_anomaly_name(self):
        return self.anomaly_name

    def get_limit(self):
        return self.limit

    def validate_fields(self):
        self.get_anomaly_no()
        self.get_anomaly_name()
        self.get_limit()

class AlarmPageQueryModel(BaseModel):
    """
    报警信息分页查询模型
    """

    anomaly_no: str = Field(default=None, description='故障模式编号')
    anomaly_name: str = Field(default=None, description='故障模式名称')
    payload_name: str = Field(default=None, description='载荷名称')
    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')
    data_type: str = Field(default='anomaly', description='数据类型：anomaly-遥测数据，eng-工程数据，parameter-参数数据')
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class AlarmRecordParaModel(BaseModel):
    """
    报警记录对应pydantic模型-参数
    """

    model_config = ConfigDict(from_attributes=True)

    uuid: str = Field(default=None, description='关键参数UUID')
    anomaly_no: str = Field(default=None, description='关键参数编号')
    anomaly_name: str = Field(default=None, description='关键参数名称')
    create_time: datetime = Field(default=None, description='规则创建时间')
    alarm_time: datetime = Field(default=None, description='报警时间')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    data_source: str = Field(default=None, description='数据来源')
    alarm_state: str = Field(default=None, description='报警状态')

    @NotBlank(field_name='uuid', message='模型uuid不能为空')
    @Size(field_name='uuid', min_length=36, max_length=36, message='部门名称长度不能超过36个字符')
    def get_uuid(self):
        return self.uuid

    @NotBlank(field_name='anomaly_no', message='关键参数编号不能为空')
    @Size(field_name='anomaly_no', min_length=1, max_length=50, message='关键参数编号长度不能超过50个字符')
    def get_anomaly_no(self):
        return self.anomaly_no

    @NotBlank(field_name='anomaly_name', message='关键参数名称不能为空')
    @Size(field_name='anomaly_name', min_length=1, max_length=100, message='关键参数名称长度不能超过100个字符')
    def get_anomaly_name(self):
        return self.anomaly_name

    @NotBlank(field_name='create_time', message='规则创建时间不能为空')
    def get_create_time(self):
        return self.create_time

    @NotBlank(field_name='alarm_time', message='报警时间不能为空')
    def get_alarm_time(self):
        return self.alarm_time

    def get_update_time(self):
        return self.update_time

    @NotBlank(field_name='data_source', message='数据来源不能为空')
    @Size(field_name='data_source', min_length=1, max_length=10, message='数据来源长度不能超过50个字符')
    def get_data_source(self):
        return self.data_source

    @NotBlank(field_name='alarm_state', message='报警状态不能为空')
    @Size(field_name='alarm_state', min_length=1, max_length=50, message='报警状态长度不能超过20个字符')
    def get_alarm_state(self):
        return self.alarm_state

    def validate_fields(self):
        self.get_uuid()
        self.get_anomaly_no()
        self.get_anomaly_name()
        self.get_create_time()
        self.get_alarm_time()
        self.get_update_time()
        self.get_data_source()
        self.get_alarm_state()


class AlarmRecordParaQueryModel(BaseModel):
    """
    报警记录查询模型-参数
    """
    time_delta: int = Field(default=None, description='查询范围')

    @NotBlank(field_name='time_delta', message='查询报警记录范围不能为空')
    def get_time_delta(self):
        return self.time_delta

    def validate_fields(self):
        self.get_time_delta()


class RecentAlarmRecordParaQueryModel(BaseModel):
    """
    查询最近报警记录查询模型-参数
    """
    anomaly_no: str = Field(..., description="故障编号")
    anomaly_name: str = Field(..., description="故障名称")
    limit: int = Field(..., ge=1, description="要获取的记录条数，最小值为1")

    @NotBlank(field_name='anomaly_no', message='查询故障编号不能为空')
    def get_anomaly_no(self):
        return self.anomaly_no

    @NotBlank(field_name='anomaly_name', message='查询故障名称不能为空')
    def get_anomaly_name(self):
        return self.anomaly_name

    def get_limit(self):
        return self.limit

    def validate_fields(self):
        self.get_anomaly_no()
        self.get_anomaly_name()
        self.get_limit()

class AlarmPageParaQueryModel(BaseModel):
    """
    报警信息分页查询模型-参数
    """

    anomaly_no: str = Field(default=None, description='关键参数编号')
    anomaly_name: str = Field(default=None, description='关键参数名称')
    payload_name: str = Field(default=None, description='载荷名称')
    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')
    data_type: str = Field(default='parameter', description='数据类型：anomaly-遥测数据，eng-工程数据，parameter-参数数据')
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')