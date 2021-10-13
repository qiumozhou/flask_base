# -*- coding: utf-8 -*-
# @Time    : 2021/9/22 下午6:39
# @Author  : mozhouqiu
# @FileName: db_session.py
# @Email    ：15717163552@163.com

from sqlalchemy.orm import sessionmaker
from db_server.init_db import engine
Session = sessionmaker(bind=engine)
