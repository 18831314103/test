from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String,LargeBinary
from config.database import Base


class AlarmData(Base):
    """
    报警记录表
    """

    __tablename__ = 'anomaly_alarm_data_table_anomaly'

    ID = Column(Integer, primary_key=True, autoincrement=True, comment='报警记录ID')
    MODEL_UUID = Column(String(36), comment='故障模式UUID')
    DATA = Column(LargeBinary, comment='报警数据')
    CREATE_TIME = Column(DateTime, comment='报警创建时间')
    UPDATE_TIME = Column(DateTime, comment='更新时间')

class AlarmDataPara(Base):
    """
    报警记录表-参数
    """

    __tablename__ = 'anomaly_alarm_data_table_parameter'

    ID = Column(Integer, primary_key=True, autoincrement=True, comment='报警记录ID')
    MODEL_UUID = Column(String(36), comment='故障模式UUID')
    DATA = Column(LargeBinary, comment='报警数据')
    CREATE_TIME = Column(DateTime, comment='报警创建时间')
    UPDATE_TIME = Column(DateTime, comment='更新时间')


class AlarmDataEng(Base):
    """
    报警记录表-工程数据
    """

    __tablename__ = 'anomaly_alarm_data_table_eng'

    ID = Column(Integer, primary_key=True, autoincrement=True, comment='报警记录ID')
    MODEL_UUID = Column(String(36), comment='故障模式UUID')
    DATA = Column(LargeBinary, comment='报警数据')
    CREATE_TIME = Column(DateTime, comment='报警创建时间')
    UPDATE_TIME = Column(DateTime, comment='更新时间')