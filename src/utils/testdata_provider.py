#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:testdata_provider.py
@time:2022/10/12
"""
import os
import queue

from src.utils.config_manager import get_root_path


def get_testdatas(testdata_file):
    """
    提供测试数据供locust使用
    :param testdata_file: 测试文件的文件名
    :return:
    """
    user_data_queue = queue.Queue()
    test_data_file = get_root_path() + os.sep + "testdata" + os.sep + testdata_file
    with open(test_data_file, 'r', encoding='utf-8') as f:
        file_data = f.readlines()
        for line in file_data:
            data = {"username": line.split(",")[0].strip(), "password": line.split(",")[1].strip()}
            user_data_queue.put_nowait(data)
    return user_data_queue


if __name__ == '__main__':
    pass
