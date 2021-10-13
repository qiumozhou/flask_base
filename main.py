# -*- coding: utf-8 -*-
# @Time    : 2021/10/13 下午4:00
# @Author  : mozhouqiu
# @FileName: main.py
# @Email    ：15717163552@163.com
from flask import request
from gevent import monkey
from gevent.pywsgi import WSGIServer
from flask_cors import CORS

import config

from utils import create_app
monkey.patch_all()
app = create_app()
CORS(app,supports_credentials=True)




@app.route('/')
def hello():
    return 'hello hx'


def run_server():
    server = WSGIServer((config.LOCAL_HOST, config.LOCAL_PORT), app)
    print("Server start on http://{host}:{port}".format(host=config.LOCAL_HOST, port=config.LOCAL_PORT))
    server.serve_forever()

if __name__ == '__main__':
    run_server()
