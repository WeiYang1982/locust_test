#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:login.py
@time:2022/09/22
"""
import base64
import os
import queue
from datetime import datetime

import bcrypt as bcrypt
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from locust import FastHttpUser, SequentialTaskSet, events

from src.utils.config_manager import get_root_path
from src.utils.request_handler import my_request_handler


class Login(SequentialTaskSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params = self.parent.user_data_queue.get()
        self.cipher_text = None
        self.cipher = None
        self.value_for_token = None
        self.header = {'X-RPA-SIGNATURE-DEBUG': 'bBkbiV1DRW+8cffTDJtOYkIczSogYPih', "Authorization": "", "username": ""}

    def get_public_key(self):
        uri = "/gateway/cs/api/public/v1/user/settings"
        with self.client.get(uri, stream=True, name='获取公钥', catch_response=True) as res:
            if res.json()['code'] == 0 and res.json()['success'] is True:
                public_pem = res.json().get("data").get("key").encode("utf-8")
                # 用公钥加密并用base64转字符
                username = self.params.get("username").strip()
                self.header.update({"username": username})
                rsa_key = RSA.importKey(public_pem)
                self.cipher = Cipher_pkcs1_v1_5.new(rsa_key)  # 创建用于执行pkcs1_v1_5加密或解密的密码
                self.cipher_text = base64.b64encode(self.cipher.encrypt(username.encode('utf-8'))).decode('utf-8')
                res.success()
            else:
                res.failure("获取公钥失败, response: " + res.text)

    def get_salt(self):
        salt_url = "/gateway/cs/api/public/v1/user/getSalt"
        value = self.cipher_text

        param = {"value": value}
        with self.client.get(salt_url, params=param, stream=True, name='获取盐值', catch_response=True) as res:
            if res.json()['code'] == 0 and res.json()['success'] is True:
                salt = res.json()["data"]["salt"]
                timeStr = res.json().get("data").get("time")
                tim = str(int(datetime.strptime(timeStr, "%Y-%m-%dT%H:%M:%S.%f+08:00").timestamp() * 1000)).encode(
                    "utf-8")
                cipher_time_text = base64.b64encode(self.cipher.encrypt(tim)).decode('utf-8')

                # 获取token
                password = self.params.get("password").strip().encode("utf-8")

                hashed = bcrypt.hashpw(password, ("$2a$10$" + salt).encode("utf-8")).decode('utf-8')
                self.value_for_token = self.cipher_text + "$s~" + hashed + ".$2" + cipher_time_text
                res.success()
            else:
                res.failure("获取盐值失败, response: " + res.text)

    def get_token(self):
        token_url = "/gateway/cs/api/public/v3/authenticate"
        token_param = {
            "authMethod": 0,
            "value": self.value_for_token
        }
        print(token_param)
        with self.client.post(token_url, json=token_param, stream=True, name="获取token", catch_response=True) as res:
            if res.json()["code"] == 0 and res.json()['success'] is True:
                token = res.json()["data"]["id_token"]
                self.header.update({"Authorization": "Bearer " + token})
                res.success()
                return token
            else:
                res.failure('获取token失败， response: ' + res.text)
                return ""

    def on_start(self):
        self.get_public_key()
        self.get_salt()
        self.get_token()


class WebUser(FastHttpUser):
    host = "http://172.19.192.44:30000"
    tasks = [Login]  # Testcase类
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
    login = Login()
    login.get_public_key()
    login.get_salt()
    login.get_token()

    pass
