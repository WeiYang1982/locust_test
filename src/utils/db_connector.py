#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:db_connector.py
@time:2022/09/27
"""
from influxdb import InfluxDBClient


class DBConnector:
    def __init__(self, host, port, db_name):
        self.db_name = db_name
        self.client = InfluxDBClient(host=host, port=port)
        self.client.switch_database(self.db_name)

    def write_to_db(self, data):
        self.client.write_points(data, time_precision='ms', database=self.db_name)


if __name__ == '__main__':
    import json
    db = DBConnector("172.20.0.74", "8086", "test")
    json_str = '[{"measurement": "ResponseTable","tags": {"hostname":"LAPTOP-OADTN6DP","requestName": "/be/api/v1/requirement/search","requestType": "GET","status":"success"},"time":"2022-09-27 07:13:32.645544+00:00","fields": {"responseTime": "148","responseLength":"0"}}]'
    json_obj = json.loads(json_str)
    db.write_to_db(json.loads(json_str))
    pass
