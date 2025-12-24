/**
 * Author: XJ
 * Date: 2025-03-27
 * Description: 统计分析模块API接口
 * */

import { request } from "@umijs/max";

/** 获取实验信息列表 GET /analyze/rule */
export async function sendExpList(
    params: {
        cabinName?: string;
        expName?: string
        rackNamePattern?: string;
        subsystemPattern?: string;
        actionNamePattern?: string;
        timeTypePattern?: string;
        submitTimeStart?: string;
        submitTimeEnd?: string;
        executeTimeStart?: string;
        executeTimeEnd?: string;
        sendTimeStart?: string;
        sendTimeEnd?: string;
        pageNo: number;
        pageSize: number;
    },
    options?: { [key: string]: any },
) {
    return request<{
        code: number;
        data: any;
        info: { count: string; page: string }[];
        msg: string;
        success: boolean;
    }>(`${API_EXP}/apisexpUrl/exp/v1/injectSend/sendExpList`, {
        method: 'GET',
        params: {
            ...params,
        },
        ...(options || {}),
    });
}
/**获取单个实验详细信息 */
export async function sendActionParaList(
    params: {
        actionEditId: string;
    },
    options?: { [key: string]: any },
) {
    return request<{
        code: number;
        data: any;
        info: { count: string; page: string }[];
        msg: string;
        success: boolean;
    }>(`${API_EXP}/apisexpUrl/exp/v1/injectSend/sendActionParaList`, {
        method: 'GET',
        params: {
            ...params,
        },
        ...(options || {}),
    });
}
/** 获取所有实验名称列表 GET /analyze/selectAll 
 * @param cabinId
 * @param expName
 * @param pageNo
 * @param pageSize
*/
export async function getExpListAPI(
    params: {
        cabinId?: string;
        expName?: string
        pageNo: number;
        pageSize: number;
    },
    options?: { [key: string]: any },
) {
    return request<{
        data: {
            code: number;
            data: { id: string; name: string; }[];
            info: { count: string; page: string }[];
            msg: string;
            success: boolean;
        };
    }>(`${API_EXP}/apisexpUrl/exp/v1/experiment/selectAll`, {
        method: 'GET',
        params: {
            ...params,
        },
        ...(options || {}),
    });
}
