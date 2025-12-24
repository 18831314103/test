from config.enums import ApiMethod
from utils.request import api_request


class AlarmRecordApi:
    """
    报警信息相关接口
    """

    @classmethod
    def list_alarm_record_in_duration(cls, query: dict):
        """
        查询报警信息

        :param query: 查询报警信息参数
        :return:
        """
        return api_request(
            url='/system/alarm_record/list',
            method=ApiMethod.GET,
            params=query,
        )

    @classmethod
    def list_recent_alarm_record(cls, anomaly_info: str):
        """
        查询最近的报警信息

        :anomaly_info: 格式为：{anomaly_no}@{anomaly_name}@{limit}
        :return:
        """
        return api_request(
            url=f'/system/alarm_record/recent/{anomaly_info}',
            method=ApiMethod.GET
        )

    @classmethod
    def search_alarm_data(cls, uuid: str, data_type: str = 'anomaly'):
        """
        查询报警数据

        :param uuid: 报警记录 uuid
        :param data_type: 数据类型: anomaly(遥测数据), parameter(参数数据), eng(工程数据)
        :return:
        """
        return api_request(
            url=f'/system/alarm_record/get_data/{uuid}',
            method=ApiMethod.GET,
            params={"data_type": data_type}
        )

    @classmethod
    def list_search_alarm_record(cls, query: dict):
        """
        查询报警信息

        :anomaly_info: 查询报警信息参数
        :return:
        """
        return api_request(
            url=f'/system/alarm_record/search',
            method=ApiMethod.GET,
            params=query,
        )

    @classmethod
    def get_param_cabin_kjz(cls, query: dict):
        """
        查询关键参数缓存的舱段设置

        :return:
        """
        return api_request(
            url=f'/getKeyPAMCabin',
            method=ApiMethod.GET,
            params=query,
        )

    @classmethod
    def set_param_cabin_kjz(cls, json: dict):
        """
        更改关键参数的舱段设置缓存信息

        :return:
        """
        return api_request(
            url='/editKeyPAMCabin',
            method=ApiMethod.POST,
            json=json,
        )

    @classmethod
    def get_all_param_data(cls):
        """
        查询全部缓存中的参数数据

        :return:
        """
        return api_request(
            url=f'/get_data',
            method=ApiMethod.POST,
            external_server="faust"
        )

    @classmethod
    def get_param_data_of_paramId(cls,json: dict):
        """
        根据参数代号获取缓存中的参数数据

        :return:
        """
        return api_request(
            url=f'/get_data',
            method=ApiMethod.POST,
            json=json,
            external_server="faust"
        )

    @classmethod
    def get_info_by_fault_nos(cls, json: dict):
        """
        根据参数代号获取故障模式详细信息

        :return:
        """
        return api_request(
            url=f'/get_info',
            method=ApiMethod.POST,
            json=json,
            external_server="faust"
        )

