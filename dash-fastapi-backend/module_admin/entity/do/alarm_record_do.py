from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from config.database import Base


class AlarmRecord(Base):
    """
    报警记录表
    """

    __tablename__ = 'anomaly_alarm_table_anomaly'

    ID = Column(Integer, primary_key=True, autoincrement=True, comment='报警记录ID')
    MODEL_UUID = Column(String(36), comment='故障模式UUID')
    ANOMALY_NO = Column(String(255), comment='故障模式编号')
    ANOMALY_NAME = Column(String(255), comment='故障模式名称')
    PAYLOAD_NAME = Column(String(255), comment='载荷名称')
    CREATE_TIME = Column(DateTime, comment='规则创建时间')
    ALARM_TIME = Column(DateTime, comment='报警时间')
    UPDATE_TIME = Column(DateTime, comment='更新时间')
    DATA_SOURCE = Column(String(10), comment='数据来源')
    ALARM_STATE = Column(String(50), comment='报警状态')

class AlarmRecordPara(Base):
    """
    报警记录表-参数
    """

    __tablename__ = 'anomaly_alarm_table_parameter'

    ID = Column(Integer, primary_key=True, autoincrement=True, comment='报警记录ID')
    MODEL_UUID = Column(String(36), comment='关键参数UUID')
    ANOMALY_NO = Column(String(255), comment='关键参数编号')
    ANOMALY_NAME = Column(String(255), comment='关键参数名称')
    PAYLOAD_NAME = Column(String(255), comment='载荷名称')
    CREATE_TIME = Column(DateTime, comment='规则创建时间')
    ALARM_TIME = Column(DateTime, comment='报警时间')
    UPDATE_TIME = Column(DateTime, comment='更新时间')
    DATA_SOURCE = Column(String(10), comment='数据来源')
    ALARM_STATE = Column(String(50), comment='报警状态')

class AlarmRecordEng(Base):
    """
    报警记录表-工程数据
    """

    __tablename__ = 'anomaly_alarm_table_eng'

    ID = Column(Integer, primary_key=True, autoincrement=True, comment='报警记录ID')
    MODEL_UUID = Column(String(36), comment='工程数据UUID')
    ANOMALY_NO = Column(String(255), comment='工程数据编号')
    ANOMALY_NAME = Column(String(255), comment='工程数据名称')
    PAYLOAD_NAME = Column(String(255), comment='载荷名称')
    CREATE_TIME = Column(DateTime, comment='规则创建时间')
    ALARM_TIME = Column(DateTime, comment='报警时间')
    UPDATE_TIME = Column(DateTime, comment='更新时间')
    DATA_SOURCE = Column(String(10), comment='数据来源')
    ALARM_STATE = Column(String(50), comment='报警状态')