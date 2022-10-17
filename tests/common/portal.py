#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:portal.py
@time:2022/10/17
"""
from locust import FastHttpUser, run_single_user
from locust import task

from src.utils.testdata_provider import get_testdatas
from tests.common.login import Login


class Logout(Login):

    @task
    def front(self):
        uri = "/portal"
        with self.client.get(uri, headers=self.header, name="首页", stream=True, catch_response=True) as res:
            print(res.text)
            if res.json()['code'] == 0:
                res.success()
            else:
                res.failure("退出失败 res: {}".format(res.text))


class WebUser(FastHttpUser):
    host = "http://172.19.192.44:30000"
    tasks = [Logout]  # Testcase类
    user_data_queue = get_testdatas("testdata.txt")
    # min_wait = 1000
    # max_wait = 3000


if __name__ == '__main__':
    run_single_user(WebUser)
    pass
