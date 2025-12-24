/**
 * Author: XJ
 * Date: 2025-04-03
 * Description: 实验申请模块API接口
 * */

import { request } from "@umijs/max";


/** 获取实验申请列表 */
export async function selectExpChild(
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
    }>(`${API_EXP}/apisexpUrl/exp/v1/experiment/selectExpChild`, {
        method: 'GET',
        params: {
            ...params,
            begTime_begin: "2025-03-27 18:04:36.678",
            begTime_end: "2025-05-03 18:04:36.678",
            name: "TGTH-19A1-00"
        },
        ...(options || {}),
    });
}