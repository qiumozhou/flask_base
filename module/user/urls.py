# -*- coding: utf-8 -*-
# @Time    : 2021/9/23 下午1:55
# @Author  : mozhouqiu
# @FileName: urls.py
# @Email    ：15717163552@163.com
from module.user.views import UserView, LoginView, UpLoadInfoView, StopView, AuthView, TokenView

USER_MODULES = [
    ("/user", UserView, "user"),
    ("/login", LoginView, "login"),
    ("/upload_info", UpLoadInfoView, "upload_info"),
    ("/stop", StopView, "stop"),
    ("/auth", AuthView, "auth"),
    ("/token", TokenView, "token")
]