/**
 * Author: XJ
 * Date: 2025-06-04
 * Description: 实验申请模块API接口
 * */

import { request } from "@umijs/max";


/** 获取xml到事件树结构 */
export async function getXmlTree(
    params: {

    },
    options?: { [key: string]: any },
) {
    return request<{
        code: number;
        data: any;
        info: { count: string; page: string }[];
        msg: string;
        success: boolean;
    }>(`${API_EXP}/api/xml/getXmlTree`, {
        method: 'GET',
        params: {
            ...params,
        },
        ...(options || {}),
    });
}
/** 根据事件ID获取参数 */
export async function getParamByActionId(
    params: {
        actionId:string
    },
    options?: { [key: string]: any },
) {
    return request<{
        code: number;
        data: any;
        info: { count: string; page: string }[];
        msg: string;
        success: boolean;
    }>(`${API_EXP}/api/xml/getParamByActionId`, {
        method: 'GET',
        params: {
            ...params,
        },
        ...(options || {}),
    });
}