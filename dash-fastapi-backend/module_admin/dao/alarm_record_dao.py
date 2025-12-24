from sqlalchemy import bindparam, func, or_, select, update, text  # noqa: F401
from sqlalchemy.sql import expression
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import immutabledict
from typing import List

# 故障
from module_admin.entity.do.alarm_record_do import AlarmRecord
from module_admin.entity.vo.alarm_record_vo import AlarmRecordQueryModel,RecentAlarmRecordQueryModel,AlarmPageQueryModel

# 参数
from module_admin.entity.do.alarm_record_do import AlarmRecordPara, AlarmRecordEng
from module_admin.entity.vo.alarm_record_vo import AlarmRecordParaQueryModel,RecentAlarmRecordParaQueryModel,AlarmPageParaQueryModel

from module_admin.entity.do.alarm_data_do import AlarmDataPara,AlarmData, AlarmDataEng
from module_admin.entity.vo.alarm_data_vo import AlarmDataSchema

from module_admin.entity.do.dept_do import SysDept
from module_admin.entity.do.role_do import SysRoleDept  # noqa: F401
from datetime import datetime,time
from utils.page_util import PageUtil



class AlarmRecordDao:
    """
    报警信息数据库操作层
    """

    @classmethod
    async def get_alarm_record_in_duration(cls, db: AsyncSession, alarm_record_info: AlarmRecordQueryModel,
                                           data_scope_sql: str):
        """
        获取报警信息列表

        :param db: orm对象
        :param alarm_record_info: 报警记录
        :param data_scope_sql: 数据权限sql
        :return:
        """
        time_delta_seconds = alarm_record_info.time_delta
        time_delta_expr = expression.text(f"INTERVAL {time_delta_seconds} SECOND")
        start_query_time = func.now() - time_delta_expr

        alarm_records = (await db.execute(
            select(AlarmRecord).where(AlarmRecord.ALARM_TIME >= start_query_time)
        )).scalars().all()

        return alarm_records

    @classmethod
    async def get_recent_alarm_records(cls, db: AsyncSession,
                                       recent_alarm_record_info:RecentAlarmRecordQueryModel,
                                       data_scope_sql: str
                                       ):
        """
        获取最近的报警记录

        :param db: orm对象
        :param limit: 要获取的记录条数，默认为5
        :return: 最近的报警记录列表
        """
        alarm_records = (
            await db.execute(
                select(AlarmRecord)
                .where(AlarmRecord.ANOMALY_NO == recent_alarm_record_info.anomaly_no)
                .where(AlarmRecord.ANOMALY_NAME == recent_alarm_record_info.anomaly_name)
                .order_by(AlarmRecord.ALARM_TIME.desc())  # 按报警时间降序排列
                .limit(recent_alarm_record_info.limit)  # 限制返回的记录条数
            )
        ).scalars().all()

        return alarm_records

    @classmethod
    async def get_alarm_list(cls, db: AsyncSession, query_object: AlarmPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取报警列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 报警列表查询对象
        """
        # 根据data_type选择不同的表
        if query_object.data_type == 'parameter':
            table = AlarmRecordPara
        elif query_object.data_type == 'eng':
            table = AlarmRecordEng
        else:
            table = AlarmRecord
            
        query = (
            select(table)
            .where(
                table.ANOMALY_NO.like(f'%{query_object.anomaly_no}%') if query_object.anomaly_no else True,
                table.ANOMALY_NAME.like(f'%{query_object.anomaly_name}%') if query_object.anomaly_name else True,
                table.PAYLOAD_NAME.like(f'%{query_object.payload_name}%') if query_object.payload_name else True,
                # table.notice_type == query_object.notice_type if query_object.notice_type else True,
                table.ALARM_TIME.between(
                    datetime.combine(datetime.strptime(query_object.begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.end_time, '%Y-%m-%d'), time(23, 59, 59)),
                )
                if query_object.begin_time and query_object.end_time
                else True,
            )
            .order_by(table.ID)
            .distinct()
        )
        alarm_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return alarm_list

    # 参数
    @classmethod
    async def get_alarm_record_in_duration_para(cls, db: AsyncSession, alarm_record_info: AlarmRecordParaQueryModel,
                                           data_scope_sql: str):
        """
        获取报警信息列表-参数

        :param db: orm对象
        :param alarm_record_info: 报警记录
        :param data_scope_sql: 数据权限sql
        :return:
        """
        time_delta_seconds = alarm_record_info.time_delta
        time_delta_expr = expression.text(f"INTERVAL {time_delta_seconds} SECOND")
        start_query_time = func.now() - time_delta_expr

        alarm_records = (await db.execute(
            select(AlarmRecordPara).where(AlarmRecordPara.ALARM_TIME >= start_query_time)
        )).scalars().all()

        return alarm_records

    @classmethod
    async def get_recent_alarm_records_para(cls, db: AsyncSession,
                                       recent_alarm_record_info: RecentAlarmRecordParaQueryModel,
                                       data_scope_sql: str
                                       ):
        """
        获取最近的报警记录-参数

        :param db: orm对象
        :param limit: 要获取的记录条数，默认为5
        :return: 最近的报警记录列表
        """
        alarm_records = (
            await db.execute(
                select(AlarmRecordPara)
                .where(AlarmRecordPara.ANOMALY_NO == recent_alarm_record_info.anomaly_no)
                .where(AlarmRecordPara.ANOMALY_NAME == recent_alarm_record_info.anomaly_name)
                .order_by(AlarmRecordPara.ALARM_TIME.desc())  # 按报警时间降序排列
                .limit(recent_alarm_record_info.limit)  # 限制返回的记录条数
            )
        ).scalars().all()

        return alarm_records

    @classmethod
    async def get_alarm_list_para(cls, db: AsyncSession, query_object: AlarmPageParaQueryModel, is_page: bool = False):
        """
        根据查询参数获取报警列表信息-参数

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 报警列表查询对象
        """
        # 根据data_type选择不同的表
        if query_object.data_type == 'parameter':
            table = AlarmRecordPara
        elif query_object.data_type == 'eng':
            table = AlarmRecordEng
        else:
            table = AlarmRecord
        
        query = (
            select(table)
            .where(
                table.ANOMALY_NO.like(f'%{query_object.anomaly_no}%') if query_object.anomaly_no else True,
                table.ANOMALY_NAME.like(f'%{query_object.anomaly_name}%') if query_object.anomaly_name else True,
                table.PAYLOAD_NAME.like(f'%{query_object.payload_name}%') if query_object.payload_name else True,
                # table.notice_type == query_object.notice_type if query_object.notice_type else True,
                table.ALARM_TIME.between(
                    datetime.combine(datetime.strptime(query_object.begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.end_time, '%Y-%m-%d'), time(23, 59, 59)),
                )
                if query_object.begin_time and query_object.end_time
                else True,
            )
            .order_by(table.ID)
            .distinct()
        )
        alarm_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return alarm_list

    @classmethod
    async def get_alarm_data_by_model_uuid(cls, db: AsyncSession, model_uuid: str, data_type: str = 'anomaly'):
        """统一查询方法"""
        if data_type == 'parameter':
            table = AlarmDataPara
        elif data_type == 'eng':
            table = AlarmDataEng
        else:
            table = AlarmData
        data_list = (await db.execute(
            select(table).where(table.MODEL_UUID == model_uuid)
        )).scalars().all()

        return [AlarmDataSchema.from_orm_with_decompress(d) for d in data_list]
