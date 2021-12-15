# -*- coding: utf-8 -*-
# @Time    : 2021/10/13 下午4:00
# @Author  : mozhouqiu
# @FileName: main.py
# @Email    ：15717163552@163.com
from gevent import monkey
from gevent.pywsgi import WSGIServer

from common.app import BaseAppFactory
from common.urls import UrlAddBase
from component.mysql.db_session import ModelToDB
from config import app_config

monkey.patch_all()
app = BaseAppFactory.create("dev")
UrlAddBase().add_class_url(app)


@app.route('/')
def hello():
    return 'hello hx'


def main():
    server = WSGIServer((app_config.LOCAL_HOST, app_config.LOCAL_PORT), app)
    print("Server start on http://{host}:{port}".format(host=app_config.LOCAL_HOST, port=app_config.LOCAL_PORT))
    server.serve_forever()

if __name__ == '__main__':
    ModelToDB.run()
    main()
