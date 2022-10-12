# -*- encoding=utf8 -*-
__author__ = "wei.yang"

import configparser
import os

MODULE_NAME = os.path.abspath(os.path.dirname(__file__)).split('src')[0]


def get_root_path():
    cur_path = os.path.abspath(os.path.dirname(__file__))
    root_path = cur_path[:cur_path.rfind(MODULE_NAME) + len(MODULE_NAME)]
    return root_path


def get_config():
    root_path = get_root_path()
    config = configparser.RawConfigParser()
    config.read(root_path + '%sbase.cfg' % os.sep, encoding='utf-8')
    return config


if __name__ == '__main__':
    print(get_root_path())
