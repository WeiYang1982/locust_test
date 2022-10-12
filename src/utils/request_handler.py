#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:request_handler.py
@time:2022/09/27
"""
import datetime
import json
import socket

import pytz
from locust import events

from src.utils.config_manager import get_config
from src.utils.db_connector import DBConnector

hostname = socket.gethostname()


@events.request.add_listener
def my_request_handler(request_type, name, response_time, response_length, response,
                       context, exception, start_time, url, **kwargs):
    db_host = get_config().get("influxdb", "host")
    db_port = get_config().get("influxdb", "port")
    db_name = get_config().get("influxdb", "name")
    connector = DBConnector(db_host, db_port, db_name)
    SUCCESS_TEMPLATE = '[{"measurement": "%s","tags": {"hostname":"%s","requestName": "%s","requestType": "%s","status":"%s"' \
                       '},"time":"%s","fields": {"responseTime": "%s","responseLength":"%s"} }]'

    FAIL_TEMPLATE = '[{"measurement": "%s","tags": {"hostname":"%s","requestName": "%s","requestType": "%s","exception":"%s","status":"%s"' \
                    '},"time":"%s","fields": {"responseTime": "%s","responseLength":"%s"} }]'
    if exception:
        json_string = FAIL_TEMPLATE % (
            "ResponseTable", hostname, name, request_type, exception, "fail",
            datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')), response_time, response_length)
        # print(json_string)
        connector.write_to_db(json.loads(json_string))
    else:
        json_string = SUCCESS_TEMPLATE % (
            "ResponseTable", hostname, name, request_type, "success",
            datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')), response_time, response_length)
        # print(json_string)
        connector.write_to_db(json.loads(json_string))


if __name__ == '__main__':
    pass
