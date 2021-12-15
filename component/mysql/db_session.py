# -*- coding: utf-8 -*-
# @Time    : 2021/12/15 下午1:48
# @Author  : mozhouqiu
# @FileName: db_session.py
# @Email    ：15717163552@163.com

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from abc import ABCMeta,abstractmethod


class MysqlMaker(metaclass=ABCMeta):
    HOST = 'localhost'
    PORT = 3306
    USERNAME = 'root'
    PASSWORD = '123456'

    @abstractmethod
    def create(self,db_name):
        pass


class MysqlEngineMaker(MysqlMaker):
    @classmethod
    def create(self, db_name):
        DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
            self.USERNAME,
            self.PASSWORD,
            self.HOST,
            self.PORT,
            db_name
        )
        try:
            engine = create_engine(DB_URI)
            return engine
        except:
            raise TypeError("Please select the correct database")


class MysqlSessionMaker(MysqlMaker):
    @classmethod
    def create(self,db_name):
        DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
            self.USERNAME,
            self.PASSWORD,
            self.HOST,
            self.PORT,
            db_name
        )
        try:
            engine = create_engine(DB_URI)
            session = sessionmaker(engine)()
            return session
        except:
            raise TypeError("Please select the correct database")

class ModelToDB:
    @classmethod
    def run(self):
        try:
            from module.user import models
            models.Base.metadata.create_all()
        except:
            raise TypeError("******Init Mysql Error*******")
