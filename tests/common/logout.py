#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:logout.py
@time:2022/10/12
"""
import os
import queue

from locust import FastHttpUser, run_single_user
from locust import task

from src.utils.config_manager import get_root_path
from tests.common.login import Login


class Logout(Login):

    @task
    def logout(self):
        uri = "/gateway/cs/api/private/v1/logout"
        with self.client.get(uri, headers=self.header, name="退出登录", stream=True, catch_response=True) as res:
            if res.json()['code'] == 0:
                res.success()
            else:
                res.failure("退出失败 res: {}".format(res.text))


class WebUser(FastHttpUser):
    host = "http://172.19.192.44:30000"
    tasks = [Logout]  # Testcase类
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
