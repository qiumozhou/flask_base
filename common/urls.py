# -*- coding: utf-8 -*-
# @Time    : 2021/9/23 下午5:22
# @Author  : mozhouqiu
# @FileName: urls.py
# @Email    ：15717163552@163.com
from module.user.urls import USER_MODULES as model


class UrlAddBase():

    def add_url_include(self,app, model, url_head=None, namespace=""):
        for url_end, cls_value, name in model:
            url_one = url_head + url_end
            as_view_name = namespace + name
            app.add_url_rule(url_one, view_func=cls_value.as_view(as_view_name))

    def add_class_url(self,app):
        self.add_url_include(app, model, url_head='/api/v1/users', namespace="user")