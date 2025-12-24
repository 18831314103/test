from server import app, redis_pool
from dash.dependencies import ClientsideFunction, Input, Output, State
import random
import json
import uuid
from dash import dcc, html
from datetime import datetime, timedelta

from api.ABNReal.alarm_record import AlarmRecordApi


@app.callback(
    Output('abn-real-watch-table', 'data', allow_duplicate=True),
    Input('abn-search-submit-button', 'nClicks'),
    [
        State('abn-search-anomaly-no-input', 'value'),
        State('abn-search-anomaly-name-input', 'value'),
        State('abn-search-payload-name-input', 'value'),
        State('abn-search-anomaly-date-range-picker', 'value'),
    ],
    prevent_initial_call=True,
)
def search_anomaly_info(nClick, anomaly_no, anomaly_name, payload_name, date_range):
    if date_range is None:
        return []
    page_num = 1
    page_size = 99999
    begin_time = date_range[0] if date_range is not None else None
    end_time = date_range[1] if date_range is not None else None
    anomaly_no = anomaly_no if anomaly_no else None
    anomaly_name = anomaly_name if anomaly_name else None
    payload_name = payload_name if payload_name else None
    query_param = dict(
        begin_time=begin_time,
        end_time=end_time,
        page_num=page_num,
        page_size=page_size,
        anomaly_no=anomaly_no,
        anomaly_name=anomaly_name,
        payload_name=payload_name
    )
    submit_search_res = AlarmRecordApi.list_search_alarm_record(query_param)



    if submit_search_res.get('code') != 200:
        return []
    res_items = submit_search_res.get('rows')
    return [
        {
            'key': f'row-{i + 1}',
            'dataIndex': i + 1,
            'ABNNo': item['ANOMALY_NO'],
            'ABNName': item['ANOMALY_NAME'],
            'payload': item['PAYLOAD_NAME'],
            'startTime': item['ALARM_TIME'],
            'updateTime': item['UPDATE_TIME'],
            'ruleVersion': [{
                'tag': f'{["稳定版本", "测试版本", "频发故障"][int(random.uniform(1, 1))]}',
                'color': f'{["volcano", "blue", "geekblue"][int(random.uniform(1, 1))]}',
            }]
        } for i, item in enumerate(res_items)
    ]


@app.callback(
    [
        Output('abn-search-anomaly-no-input', 'value'),
        Output('abn-search-anomaly-name-input', 'value'),
        Output('abn-search-payload-name-input', 'value'),
        Output('abn-search-anomaly-date-range-picker', 'value'),
        Output('abn-real-watch-table', 'data', allow_duplicate=True),
    ],
    Input('abn-search-reset-button', 'nClicks'),
    prevent_initial_call=True,

)
def reset_search_info(nClick):
    today = datetime.now()
    seven_days_ago = today - timedelta(days=7)
    return [None, None, None, [seven_days_ago.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')], []]
