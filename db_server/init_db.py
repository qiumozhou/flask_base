# -*- coding: utf-8 -*-
# @Time    : 2021/9/22 下午4:02
# @Author  : mozhouqiu
# @FileName: init_connection.py
# @Email    ：15717163552@163.com

from sqlalchemy import create_engine

from config import MYSQL_PWD, MYSQL_DB
from db_server.models import Base

engine = create_engine('mysql+pymysql://root:{}@127.0.0.1:3306/{}?charset=utf8'.format(MYSQL_PWD,MYSQL_DB))

Base.metadata.create_all(engine)



