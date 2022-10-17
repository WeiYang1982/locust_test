#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:requirements.py
@time:2022/09/26
"""
import os
import queue

from locust import FastHttpUser, tag
from locust import task, run_single_user

from src.utils.testdata_provider import get_testdatas
from tests.common.login import Login


@tag("requirement")
class SearchRequirement(Login):

    @task
    def search_requirement(self):
        uri = "/be/api/v1/requirement/search"
        param = {
            "page": 1,
            "size": 10,
            "name": "",
            "excludeStatus": 1,
            "sort": "modifiedAt,desc",
            "createBy": "",
            "stageStatus": ""
        }
        with self.client.get(uri, param=param, headers=self.header, stream=True, catch_response=True) as res:
            if res.json()['code'] == 0:
                res.success()
            else:
                res.failure("搜索失败 res:{}".format(res.text))

    @task
    def get_todo_tasks(self):
        uri = "/be/hyperpm/task/v2/tasks"
        param = {
            "page": 1,
            "size": 10,
            "user": "admin"
        }
        with self.client.get(uri, headers=self.header, param=param, stream=True, catch_response=True) as res:
            if res.json()['success'] is True:
                res.success()
            else:
                res.failure("搜索失败 res:{}".format(res.text))


class WebUser(FastHttpUser):
    host = "http://172.19.192.44:30000"
    tasks = [SearchRequirement]  # Testcase类
    user_data_queue = get_testdatas("testdata.txt")
    min_wait = 0
    max_wait = 0


if __name__ == '__main__':
    run_single_user(WebUser)
    pass
