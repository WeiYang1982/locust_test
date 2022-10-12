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

from tests.common.login import Login
from src.utils.config_manager import get_root_path


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
    """性能测试配置 换算配置"""
    host = "http://172.19.192.44:30000"
    tasks = [SearchRequirement]  # Testcase类
    user_data_queue = queue.Queue()
    test_data_file = get_root_path() + os.sep + "testdata" + os.sep + "testdata.txt"
    with open(test_data_file, 'r', encoding='utf-8') as f:
        file_data = f.readlines()
        for line in file_data:
            data = {"username": line.split(",")[0].strip(), "password": line.split(",")[1].strip()}
            user_data_queue.put_nowait(data)
    min_wait = 1000
    max_wait = 3000


if __name__ == '__main__':
    run_single_user(WebUser)
    pass
