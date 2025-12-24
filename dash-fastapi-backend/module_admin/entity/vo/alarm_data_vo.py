from pydantic import BaseModel
from typing import Optional
import base64
from datetime import datetime
from pydantic_validation_decorator import Network, NotBlank, Size
import pickle
import zlib


class AlarmDataSchema(BaseModel):
    """报警数据序列化模型"""
    ID: int
    MODEL_UUID: str
    DATA: list
    CREATE_TIME: Optional[datetime]
    UPDATE_TIME: Optional[datetime]

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_with_decompress(cls, obj):
        """
        将 BLOB(bytes) 先解压再反序列化成原始对象
        """
        if obj.DATA:
            try:
                decompressed = zlib.decompress(obj.DATA)
                data_obj = pickle.loads(decompressed)
            except Exception as e:
                data_obj = None
        else:
            data_obj = None

        return cls(
            ID=obj.ID,
            MODEL_UUID=obj.MODEL_UUID,
            DATA=data_obj,
            CREATE_TIME=obj.CREATE_TIME,
            UPDATE_TIME=obj.UPDATE_TIME
        )

class AlarmDataQuery(BaseModel):
    uuid: str
    @NotBlank(field_name='uuid', message='uuid不能为空')
    def get_uuid(self):
        return self.uuid

    def validate_fields(self):
        self.get_uuid()