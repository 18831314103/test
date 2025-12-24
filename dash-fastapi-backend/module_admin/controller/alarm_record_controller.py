from datetime import datetime
from fastapi import APIRouter, Depends, Query, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.data_scope import GetDataScope
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.alarm_record_vo import AlarmRecordQueryModel, AlarmRecordModel,RecentAlarmRecordQueryModel,AlarmPageQueryModel
from module_admin.entity.vo.alarm_record_vo import AlarmRecordParaQueryModel, AlarmRecordParaModel,RecentAlarmRecordParaQueryModel,AlarmPageParaQueryModel
from module_admin.entity.vo.alarm_data_vo import AlarmDataSchema,AlarmDataQuery
from module_admin.service.alarm_record_service import AlarmRecordService
from module_admin.service.login_service import LoginService
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


alarmRecordController = APIRouter(prefix='/system/alarm_record', dependencies=[Depends(LoginService.get_current_user)])


@alarmRecordController.get(
    '/list',
    response_model=List[AlarmRecordModel],
    dependencies=[Depends(CheckUserInterfaceAuth('system:alarm_record:list'))],
)
async def get_alarm_record_in_duration_for_show(
        request: Request,
        alarm_record_query: AlarmRecordQueryModel = Query(),
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('SysDept')),
):
    # alarm_record_query = AlarmRecordQueryModel(time_delta=time_delta)
    alarm_record_query_result = await AlarmRecordService.get_alarm_record_in_duration_services(query_db,
                                                                                               alarm_record_query,
                                                                                               data_scope_sql)
    logger.info('获取故障信息成功')

    return ResponseUtil.success(data=alarm_record_query_result)

@alarmRecordController.get(
    '/recent/{anomaly_info}',
    response_model=List[AlarmRecordModel],
    dependencies=[Depends(CheckUserInterfaceAuth('system:alarm_record:list'))],
)
async def get_recent_alarm_record_for_show(
        request: Request,
        anomaly_info: str, # 格式为：f"{anomaly_no}@{anomaly_name}@{limit}"
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('SysDept')),
):
    print(anomaly_info)
    anomaly_no, anomaly_name, limit = anomaly_info.split("@")
    limit = int(limit.replace(" ", ""))
    anomaly_name = anomaly_name.replace("&&", "/")
    recent_alarm_record_query = RecentAlarmRecordQueryModel(anomaly_no=anomaly_no, anomaly_name=anomaly_name, limit=limit)
    recent_alarm_record_query_result = await AlarmRecordService.get_recent_alarm_records_services(query_db,
                                                                                               recent_alarm_record_query,
                                                                                               data_scope_sql)
    logger.info(f'获取最近{limit}条故障信息成功|{anomaly_no} {anomaly_name}')

    return ResponseUtil.success(data=recent_alarm_record_query_result)

@alarmRecordController.get(
    '/search', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:alarm_record:list'))]
)
async def get_search_alarm_list(
    request: Request,
    notice_page_query: AlarmPageQueryModel = Query(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    search_alarm_query_result = await AlarmRecordService.get_alarm_list_services(query_db, notice_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=search_alarm_query_result)



# 参数

@alarmRecordController.get(
    '/list_para',
    response_model=List[AlarmRecordParaModel],
    dependencies=[Depends(CheckUserInterfaceAuth('system:alarm_record:list'))],
)
async def get_alarm_record_in_duration_for_show(
        request: Request,
        alarm_record_query: AlarmRecordQueryModel = Query(),
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('SysDept')),
):
    # alarm_record_query = AlarmRecordQueryModel(time_delta=time_delta)
    alarm_record_query_result = await AlarmRecordService.get_alarm_record_in_duration_services_para(query_db,
                                                                                               alarm_record_query,
                                                                                               data_scope_sql)
    logger.info('获取故障信息成功')

    return ResponseUtil.success(data=alarm_record_query_result)

@alarmRecordController.get(
    '/recent_para/{anomaly_info}',
    response_model=List[AlarmRecordParaModel],
    dependencies=[Depends(CheckUserInterfaceAuth('system:alarm_record:list'))],
)
async def get_recent_alarm_record_for_show(
        request: Request,
        anomaly_info: str, # 格式为：f"{anomaly_no}@{anomaly_name}@{limit}"
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('SysDept')),
):
    print(anomaly_info)
    anomaly_no, anomaly_name, limit = anomaly_info.split("@")
    limit = int(limit.replace(" ", ""))
    anomaly_name = anomaly_name.replace("&&", "/")
    recent_alarm_record_query = RecentAlarmRecordQueryModel(anomaly_no=anomaly_no, anomaly_name=anomaly_name, limit=limit)
    recent_alarm_record_query_result = await AlarmRecordService.get_recent_alarm_records_services_para(query_db,
                                                                                               recent_alarm_record_query,
                                                                                               data_scope_sql)
    logger.info(f'获取最近{limit}条故障信息成功|{anomaly_no} {anomaly_name}')

    return ResponseUtil.success(data=recent_alarm_record_query_result)

@alarmRecordController.get(
    '/search_para', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:alarm_record:list'))]
)
async def get_search_alarm_list(
    request: Request,
    notice_page_query: AlarmPageParaQueryModel = Query(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    search_alarm_query_result = await AlarmRecordService.get_alarm_list_services_para(query_db, notice_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=search_alarm_query_result)


@alarmRecordController.get(
    '/get_data/{uuid}',
    response_model=List[AlarmDataSchema],
    dependencies=[Depends(CheckUserInterfaceAuth('system:alarm_record:list'))]
)
async def get_search_alarm_data(
    uuid: str,
    data_type: str = Query('anomaly', description="数据类型: anomaly(遥测数据), parameter(参数数据), eng(工程数据)"),
    query_db: AsyncSession = Depends(get_db),
):
    """获取故障数据"""
    alarm_data_query = AlarmDataQuery(uuid=uuid)
    result = await AlarmRecordService.get_alarm_data_services(query_db, alarm_data_query, data_type=data_type)
    return ResponseUtil.success(data=result)

