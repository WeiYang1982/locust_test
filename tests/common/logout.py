#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:logout.py
@time:2022/10/12
"""

from locust import FastHttpUser, run_single_user
from locust import task

from src.actions.login import LoginAction
from src.utils.testdata_provider import get_testdatas


class Logout(LoginAction):

    @task
    def logout(self):
        uri = "/gateway/cs/api/private/v1/logout"
        with self.client.get(uri, headers=self.header, name="退出登录", stream=True, catch_response=True) as res:
            if res.status_code == 200:
                if res.json()['code'] == 0:
                    res.success()
                else:
                    res.failure("退出失败 res: {}".format(res.text))
            else:
                res.failure("退出失败 status_code: {}".format(res.status_code))

    def on_start(self):
        self.get_public_key()
        self.get_salt()
        self.get_token()


class WebUser(FastHttpUser):
    host = "http://10.20.16.157:30000"
    tasks = [Logout]  # Testcase类
    user_data_queue = get_testdatas("testdata.txt")
    # min_wait = 1000
    # max_wait = 3000
    min_wait = 0
    max_wait = 0


if __name__ == '__main__':
    run_single_user(WebUser)
    pass
