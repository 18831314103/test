import json

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from config.enums import RedisInitKeyConfig
from exceptions.exception import ServiceException
from module_admin.dao.config_dao import ConfigDao
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.entity.vo.config_vo import ConfigModel, ConfigPageQueryModel, DeleteConfigModel
from utils.common_util import export_list2excel, SqlalchemyUtil


class KeyPAMService:
    """
    关键参数管理服务层
    """

    @classmethod
    async def edit_key_PAM_services(cls, request: Request):
        """
        插入字典缓存信息service

        :param request: Request对象
        :param query_db: orm对象
        :return: 插入字典缓存校验结果
        """
        # 获取以key_pam:开头的键列表
        data = await request.json()
        username = data["username"]
        if username:
            await request.app.state.redis.set(f'{RedisInitKeyConfig.KEY_PAM.key}:{username}',
                                              json.dumps({"select_cabin":data["cabin"]}))
            return CrudResponseModel(is_success=True, message='修改成功')
        else:
            return CrudResponseModel(is_success=False, message='修改失败')

    @classmethod
    async def get_key_PAM_services(cls, request: Request):
        """
        根据userId获取关键参数的缓存

        :param request: Request对象
        :param query_db: orm对象
        :return: 关键参数的缓存
        """
        # 获取以key_pam:开头的键列表
        keys = await request.app.state.redis.keys(f'{RedisInitKeyConfig.KEY_PAM.key}:*')
        username = request.query_params.get("username")
        if f'{RedisInitKeyConfig.KEY_PAM.key}:{username}' not in keys:
            await request.app.state.redis.set(f'{RedisInitKeyConfig.KEY_PAM.key}:{username}',
                                              json.dumps({"select_cabin": ["TGTH", "TGWT", "TGMT"]}))
            return CrudResponseModel(is_success=True, message='获取成功', result=["TGTH", "TGWT", "TGMT"])
        else:
            username_cache = json.loads(await request.app.state.redis.get(f'{RedisInitKeyConfig.KEY_PAM.key}:{username}'))
            if "select_cabin" not in username_cache:
                username_cache["select_cabin"] = ["TGTH", "TGWT", "TGMT"]
                await request.app.state.redis.set(f'{RedisInitKeyConfig.KEY_PAM.key}:{username}',
                                                  json.dumps(username_cache))
                return CrudResponseModel(is_success=True, message='获取成功',
                                         result=["TGTH", "TGWT", "TGMT"])
            else:
                return CrudResponseModel(is_success=True, message='获取成功',
                                         result=username_cache["select_cabin"])
