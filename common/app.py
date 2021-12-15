# -*- coding: utf-8 -*-
# @Time    : 2021/12/15 上午11:25
# @Author  : mozhouqiu
# @FileName: app.py
# @Email    ：15717163552@163.com
from abc import ABCMeta,abstractmethod

from flask import Flask
from flask_cors import CORS


class AppFactory(metaclass=ABCMeta):
    @abstractmethod
    def create(self,production):
        pass


class AppProduct(metaclass=ABCMeta):
    app = Flask(__name__)

    @abstractmethod
    def init_app(self):
        pass


class BaseAppFactory(AppFactory):
    @classmethod
    def create(self,production):
        if production=="dev":
            return DevApp().init_app()
        if production=="pro":
            return ProApp().init_app()
        else:
            raise TypeError("Please select a suitable environment")


from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    """自定义正则转换器"""

    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


class DevApp(AppProduct):
    def init_app(self):
        self.app.url_map.converters['re'] = RegexConverter
        self.app.config["DEBUG"] = True
        self.app.config["TESTING"] = False
        self.app.config["SECRET_KEY"] ='!\x81\xad\x95d\x99w\x07\x89\xe4\xb7\xe0G\xe1\xbc\x85\x84\xcb\x0equ\xe4\x80\x95'
        CORS(self.app, supports_credentials=True)
        return self.app


class ProApp(AppProduct):
    def init_app(self):
        self.app.url_map.converters['re'] = RegexConverter
        self.app.config["DEBUG"] = False
        self.app.config["TESTING"] = False
        self.app.config["SECRET_KEY"] = 'x\xa6\xcc%\xcaMN*\x7f\x1b\xce\xaex*\x97P\xad\x9f\x08\x9e\x99\xc1h\xd3'
        CORS(self.app, supports_credentials=True)
        return self.app