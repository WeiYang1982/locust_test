#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:login.py
@time:2022/09/22
"""

from locust import FastHttpUser, task, run_single_user

from src.actions.login import LoginAction
from src.utils.testdata_provider import get_testdatas


class Login(LoginAction):

    @task
    def public_key(self):
        self.get_public_key()

    @task
    def salt(self):
        self.get_salt()

    @task
    def token(self):
        self.get_token()

    def on_start(self):
        self.get_public_key()
        self.get_salt()
        self.get_token()


class WebUser(FastHttpUser):
    host = "http://172.19.192.44:30000"
    tasks = [Login]  # Testcase类
    user_data_queue = get_testdatas("testdata.txt")
    min_wait = 0
    max_wait = 0


if __name__ == '__main__':
    run_single_user(WebUser)
    pass
