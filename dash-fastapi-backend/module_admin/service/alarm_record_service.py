from sqlalchemy.ext.asyncio import AsyncSession
from config.constant import CommonConstant
from exceptions.exception import ServiceException, ServiceWarning
from module_admin.dao.alarm_record_dao import AlarmRecordDao
from module_admin.entity.vo.common_vo import CrudResponseModel

# 故障
from module_admin.entity.do.alarm_record_do import AlarmRecord
from module_admin.entity.vo.alarm_record_vo import AlarmRecordQueryModel,AlarmPageQueryModel

# 参数
from module_admin.entity.do.alarm_record_do import AlarmRecordPara
from module_admin.entity.vo.alarm_record_vo import AlarmRecordParaQueryModel,AlarmPageParaQueryModel

from module_admin.entity.vo.alarm_data_vo import AlarmDataQuery

from utils.common_util import SqlalchemyUtil


class AlarmRecordService:
    """
    报警信息模块服务层
    """

    @classmethod
    async def get_alarm_record_in_duration_services(cls, query_db: AsyncSession, page_object: AlarmRecordQueryModel, data_scope_sql: str):
        """
        获取报警信息信息service

        :param query_db: orm对象
        :param page_object: 查询参数对象
        :param data_scope_sql: 数据权限对应的查询sql语句
        :return: 查询范围内报警信息列表
        """
        alarm_record_list_result = await AlarmRecordDao.get_alarm_record_in_duration(query_db, page_object, data_scope_sql)

        return alarm_record_list_result


    @classmethod
    async def get_recent_alarm_records_services(cls, query_db: AsyncSession, page_object: AlarmRecordQueryModel, data_scope_sql: str):
        """
        获取最近报警信息service

        :param query_db: orm对象
        :param page_object: 查询参数对象
        :param data_scope_sql: 数据权限对应的查询sql语句
        :return: 查询范围内报警信息列表
        """
        recent_alarm_records_list_result = await AlarmRecordDao.get_recent_alarm_records(query_db, page_object, data_scope_sql)

        return recent_alarm_records_list_result

    @classmethod
    async def get_alarm_list_services(
        cls, query_db: AsyncSession, query_object: AlarmPageQueryModel, is_page: bool = True
    ):
        """
        获取报警列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 报警列表信息对象
        """
        alarm_list_result = await AlarmRecordDao.get_alarm_list(query_db, query_object, is_page)

        return alarm_list_result



    # 参数

    @classmethod
    async def get_alarm_record_in_duration_services_para(cls, query_db: AsyncSession, page_object: AlarmRecordParaQueryModel,
                                                    data_scope_sql: str):
        """
        获取报警信息信息service

        :param query_db: orm对象
        :param page_object: 查询参数对象
        :param data_scope_sql: 数据权限对应的查询sql语句
        :return: 查询范围内报警信息列表
        """
        alarm_record_list_result = await AlarmRecordDao.get_alarm_record_in_duration_para(query_db, page_object,
                                                                                     data_scope_sql)

        return alarm_record_list_result

    @classmethod
    async def get_recent_alarm_records_services_para(cls, query_db: AsyncSession, page_object: AlarmRecordParaQueryModel,
                                                data_scope_sql: str):
        """
        获取最近报警信息service

        :param query_db: orm对象
        :param page_object: 查询参数对象
        :param data_scope_sql: 数据权限对应的查询sql语句
        :return: 查询范围内报警信息列表
        """
        recent_alarm_records_list_result = await AlarmRecordDao.get_recent_alarm_records_para(query_db, page_object,
                                                                                         data_scope_sql)

        return recent_alarm_records_list_result

    @classmethod
    async def get_alarm_list_services_para(
            cls, query_db: AsyncSession, query_object: AlarmPageParaQueryModel, is_page: bool = True
    ):
        """
        获取报警列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 报警列表信息对象
        """
        alarm_list_result = await AlarmRecordDao.get_alarm_list_para(query_db, query_object, is_page)

        return alarm_list_result

    @classmethod
    async def get_alarm_data_services(cls, db: AsyncSession, alarm_query: AlarmDataQuery, data_type: str = 'anomaly'):
        return await AlarmRecordDao.get_alarm_data_by_model_uuid(db, alarm_query.uuid, data_type=data_type)
