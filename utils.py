# -*- coding: utf-8 -*-
# @Time    : 2021/9/23 下午5:28
# @Author  : mozhouqiu
# @FileName: utils.py
# @Email    ：15717163552@163.com
from flask import Flask, jsonify
from werkzeug.routing import BaseConverter

from urls import add_class_url


class RegexConverter(BaseConverter):
    """自定义正则转换器"""

    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


def create_app():
    app = Flask(__name__)

    # 向app中添加自定义的路由转换器
    app.url_map.converters['re'] = RegexConverter

    # 挂载类视图
    add_class_url(app)

    return app

