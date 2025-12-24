from fastapi import APIRouter, Request
from utils.response_util import ResponseUtil
from utils.log_util import logger
from module_admin.annotation.log_annotation import Log
from config.enums import BusinessType
from module_admin.service.key_PAM_service import KeyPAMService

keyPAMController = APIRouter()

@keyPAMController.post('/editKeyPAMCabin')
async def editKeyPAMCabin(request: Request):
    insert_key_PAM_result = await KeyPAMService.edit_key_PAM_services(request)
    logger.info(insert_key_PAM_result.message)

    return ResponseUtil.success(msg=insert_key_PAM_result.message)

@keyPAMController.get('/getKeyPAMCabin')
async def getKeyPAMCabin(request: Request):
    insert_key_PAM_result = await KeyPAMService.get_key_PAM_services(request)
    logger.info(insert_key_PAM_result.message)

    return ResponseUtil.success(msg=insert_key_PAM_result.message,data=insert_key_PAM_result.result)
