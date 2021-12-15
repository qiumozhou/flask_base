# -*- coding: utf-8 -*-
# @Time    : 2021/9/23 下午1:53
# @Author  : mozhouqiu
# @FileName: views.py
# @Email    ：15717163552@163.com
import json

from flask import request
from flask.views import MethodView

from common.plugins import res_json
from module.user.service import UserService


class UserView(MethodView):

    def __init__(self):
        super(UserView, self).__init__()

    def post(self):
        """
            @api {POST} /api/v1/users/user 用户注册
            @apiDescription 用户注册
            @apiVersion 2.2.1
            @apiName user_register
            @apiGroup User

            @apiExample {curl} Request Example:
            curl -X POST '{{server}}:{{port}}/api/v1/users/user'

            @apiParam {String} username 用户名
            @apiParam {String} position 职位
            @apiParam {String} company_name 公司名称
            @apiParam {String} password 密码
            @apiParam {String} email 邮箱
            @apiParam {String} tel 电话号码


            @apiParamExample {json} Request Example:
            {"username":"test",
            "position":"CEO",
            "company_name":"上海宾通智能科技有限公司",
            "password":"123456",
            "email":"test@.com",
            "tel":13777777777,}


            @apiSuccess {Number} code 状态码
            @apiSuccess {String} message 消息


            @apiSuccessExample {json} Response Example:
               HTTP/1.1 0 OK
              {
            "code": 0,
            "message": "Success"
        }
        """
        data_dict = json.loads(request.data)
        res = UserService().add_user(**data_dict)
        return res_json(res)


class LoginView(MethodView):

    def __init__(self):
        super(LoginView, self).__init__()

    def post(self):
        """
           @api {POST} /api/v1/users/login 用户登录
           @apiDescription 用户登录
           @apiVersion 2.2.1
           @apiName user_login
           @apiGroup User

           @apiExample {curl} Request Example:
           curl -X POST '{{server}}:{{port}}/api/v1/users/login'

           @apiParam {String} username 用户名
           @apiParam {String} password 密码

           @apiParamExample {json} Request Example:
           {"username":"test",
           "password":"123456"}

           @apiSuccess {Number} code 状态码
           @apiSuccess {String} message 消息
           @apiSuccess {String} token token

           @apiSuccessExample {json} Response Example:
              HTTP/1.1 0 OK
             {
                   "code": 0,
                   "message": "Success",
                   "data":{
                   "token":"eyJhbGciOiJIUzUxMiI
                   sImlhdCI6MTYzMjgxMjgyNCwiZXhwI
                   joxNjMyODQ4ODI0fQ.eyJ1c2VybmFtZ
                   SI6InFteiJ9.Aj3AzvZZg40WoksWRfLVK
                   M2HWoseZPlxt3FJg87r-ZkKAqw9vmBdIGPn
                   8RzWDk18gA7Oig20a-THa7vCPP-P6g"}
               }
               """
        data_dict = json.loads(request.data)
        res = UserService().login(data_dict['username'],data_dict['password'])
        return res_json(res)


class UpLoadInfoView(MethodView):

    def __init__(self):
        super(UpLoadInfoView, self).__init__()

    def post(self):
        data_dict = json.loads(request.data)
        res = UserService().upload_info(**data_dict)
        return res_json(res)

class StopView(MethodView):

    def __init__(self):
        super(StopView, self).__init__()

    def post(self):
        data_dict = json.loads(request.data)
        res = UserService().stop_user_server(**data_dict)
        return res_json(res)


class AuthView(MethodView):

    def __init__(self):
        super(AuthView, self).__init__()

    def get(self):
        """
       @api {GET} /api/v1/users/auth 用户认证
       @apiDescription 用户认证
       @apiVersion 2.2.1
       @apiName user_auth
       @apiGroup User

       @apiExample {curl} Request Example:
       curl -X GET '{{server}}:{{port}}/api/v1/users/auth'

       @apiSuccess {Number} code 状态码
       @apiSuccess {String} message 消息
       @apiSuccess {String} name_space 命名空间
       @apiSuccess {String} username 用户名

       @apiSuccessExample {json} Response Example:
          HTTP/1.1 0 OK
         {
            "code": 0,
            "data": {
                "name_space": "bito-tkueok",
                "username": "qmz"
            },
            "msg": "success"
        }
           """
        res = UserService().get_userinfo_by_token(request)
        return res_json(res)


class TokenView(MethodView):

    def __init__(self):
        super(TokenView, self).__init__()

    def post(self):
        """
           @api {POST} /api/v1/users/token 获取token
           @apiDescription 获取token
           @apiVersion 2.2.1
           @apiName user_token
           @apiGroup User

           @apiExample {curl} Request Example:
           curl -X POST '{{server}}:{{port}}/api/v1/users/token'

           @apiParam {String} username 用户名
           @apiParam {String} password 密码

           @apiParamExample {json} Request Example:
           {"username":"test",
           "password":"123456"}

           @apiSuccess {Number} code 状态码
           @apiSuccess {String} message 消息
           @apiSuccess {String} token token
           @apiSuccess {Number} is_init 0 代表hx服务未初始化, 1 代表hx服务已初始化

           @apiSuccessExample {json} Response Example:
              HTTP/1.1 0 OK
             {
                   "code": 0,
                   "message": "Success",
                   "data":{
                   "token":"eyJhbGciOiJIUzUxMiI
                   sImlhdCI6MTYzMjgxMjgyNCwiZXhwI
                   joxNjMyODQ4ODI0fQ.eyJ1c2VybmFtZ
                   SI6InFteiJ9.Aj3AzvZZg40WoksWRfLVK
                   M2HWoseZPlxt3FJg87r-ZkKAqw9vmBdIGPn
                   8RzWDk18gA7Oig20a-THa7vCPP-P6g",
                   "is_init":1}
               }
               """
        data_dict = json.loads(request.data)
        res = UserService().get_token(data_dict['username'],data_dict['password'])
        return res_json(res)
