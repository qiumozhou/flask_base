# -*- coding: utf-8 -*-
# @Time    : 2021/9/22 下午4:00
# @Author  : mozhouqiu
# @FileName: models.py
# @Email    ：15717163552@163.com
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base

from component.mysql.db_session import MysqlEngineMaker
Base = declarative_base(MysqlEngineMaker.create("flask"))

from sqlalchemy import Column, Integer, String, DateTime
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    __tablename__ = 'tb_user'
    id = Column(Integer, primary_key=True)
    username = Column(String(150,collation="utf8_bin"), unique=True)
    _password_hash = Column(String(128))
    email = Column(String(255),nullable=True)
    tel = Column(String(255), nullable=True)
    is_active = Column(Integer, default=1)
    super_admin = Column(Integer, default=1)
    last_login_time = Column("last_login_time", DateTime, nullable=True)
    create_time = Column("create_time", DateTime, nullable=True, default=datetime.now())
    nickname = Column(String(255), nullable=True)
    type = Column(String(255), nullable=True)
    position = Column(String(32), nullable=True)
    company_name = Column(String(100), nullable=True)
    is_lock = Column(String(255), nullable=True)
    name_space = Column(String(150), nullable=True)
    ip = Column(String(32), nullable=True)
    store_path = Column(String(150), nullable=True)
    file_name = Column(String(150), nullable=True)

    @property
    def password(self):
        raise Exception("password can't read")

    @password.setter
    def password(self, value):
        self._password_hash = generate_password_hash(value)

    def check_password(self, value):
        return check_password_hash(self._password_hash, value)


