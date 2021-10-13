# -*- coding: utf-8 -*-
# @Time    : 2021/9/23 下午1:55
# @Author  : mozhouqiu
# @FileName: service.py
# @Email    ：15717163552@163.com
import os
import time

from config import SECRET_KEY, EXPIRATION
from db_server.db_session import Session
from db_server.models import User
from plugins import to_dict, custom_field
from user.res_code import USER_REPEAT, SUCCESS, USER_ERROR, NO_TOKEN, SERVER_NOT_RUNNING
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature


class UserService:

    def __init__(self):
        self._session = Session()

    def add_user(self,**user_data):
        user_obj = self._session.query(User).filter(User.username==user_data["username"]).first()
        if user_obj:
            return USER_REPEAT
        user_data["name_space"] = self.username_to_namespace()
        self._session.add(User(**user_data))
        self._session.commit()
        self._session.close()
        return SUCCESS

    def username_to_namespace(self):
        import random
        seed = 'zyxwvutsrqponmlkjihgfedcba'
        sa = []
        for i in range(6):
            sa.append(random.choice(seed))
        name = ''.join(sa)
        namespace = "bito-"+ name
        return namespace

    def login(self,username,passwd):
        userobj = self._session.query(User).filter(User.username==username).first()
        state = userobj.file_name
        name = userobj.username
        if not userobj or not userobj.check_password(passwd):
            return USER_ERROR
        s = Serializer(SECRET_KEY, expires_in=EXPIRATION)
        self.init_user_pod(username)
        return SUCCESS,{"token":s.dumps({'username': name}).decode(),"is_init":1 if state else 0}

    def get_token(self,username,passwd):
        userobj = self._session.query(User).filter(User.username==username).first()
        if userobj:
            state = userobj.file_name
            name = userobj.username
            if not userobj or not userobj.check_password(passwd):
                return USER_ERROR
            s = Serializer(SECRET_KEY, expires_in=EXPIRATION)
            return SUCCESS,{"token":s.dumps({'username': name}).decode(),"is_init":1 if state else 0}
        else:
            return SERVER_NOT_RUNNING

    def init_user_pod(self,username):
        userobj = self._session.query(User).filter(User.username==username).first()
        if not userobj.ip and not userobj.file_name:
            ConfigService().run(userobj.name_space,restart=False)
            userobj.file_name = 1
            self._session.commit()
            self._session.close()
        if not userobj and userobj.file_name:
            ConfigService().run(userobj.name_space,restart=True)


    def upload_info(self,**kwargs):
        userobj = self._session.query(User).filter(User.name_space==kwargs.get("name_space")).first()
        userobj.ip = kwargs.get("pod_ip")
        self._session.commit()
        self._session.close()
        return SUCCESS

    def stop_user_server(self,**kwargs):
        userobj = self._session.query(User).filter(User.name_space==kwargs.get("name_space")).first()
        userobj.ip=""
        self._session.delete(userobj)
        self._session.commit()
        self._session.close()
        ConfigService().stop(userobj.name_space)
        return SUCCESS

    def get_userinfo_by_token(self,request):
        try:
            token = request.headers["Token"]
        except:
            return NO_TOKEN
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
            userobj = self._session.query(User).filter(User.username==data["username"]).first()
            data = custom_field(["username","name_space"],to_dict(userobj))
            return SUCCESS,data
        # token过期
        except SignatureExpired:
            return None
        # token错误
        except BadSignature:
            return None

class ConfigService:

    def __init__(self):
        self._work_path = "/home/hxali/deployment"
        self._pwd = "bitorobotics"
        self._namespace = None

    def init_name_space(self,namespace):
        self._namespace = namespace
        os.system(
            "kubectl create namespace {}".format(self._namespace))

    # def init_pv(self):
    #     os.system("cd {} && kubectl apply -f {} -n {}".format(self._work_path,"pv.yaml",self._namespace))

    def init_pvc(self):
        # os.system(
        #     "echo {}|sudo su root".format(self._pwd))
        # os.chdir('/')
        os.system("cd {} && kubectl apply -f {} -n {}".format(self._work_path,"pvc.yaml",self._namespace))
        time.sleep(1)
        os.system("cd {} && kubectl apply -f {} -n {}".format(self._work_path, "pvc_pcd.yaml", self._namespace))
        time.sleep(1)
        os.system("cd {} && kubectl apply -f {} -n {}".format(self._work_path, "pvc_image.yaml", self._namespace))
        time.sleep(1)
        os.system("cd {} && kubectl apply -f {} -n {}".format(self._work_path, "pvc_txt.yaml", self._namespace))



    def init_server_first(self):
        # os.system(
        #     "echo {}|sudo su root".format(self._pwd))
        # os.chdir('/')
        os.system("cd {} && kubectl apply -f {} -n {}".format(self._work_path,"main.yaml",self._namespace))

    def init_server_not_first(self):
        # os.system(
        #     "echo {}|sudo su root".format(self._pwd))
        # os.chdir('/')
        os.system("cd {} && kubectl apply -f {} -n {}".format(self._work_path,"main_restart.yaml",self._namespace))

    def delete_server(self,namespace):
        os.system("cd {} && kubectl delete -f {} -n {}".format(self._work_path, "main.yaml", namespace))
        time.sleep(10)

    def delete_name(self):
        os.system("cd {} && kubectl delete namespace {}".format(self._work_path,self._namespace))
        time.sleep(5)

    def delete_pv(self):
        os.system("cd {} && kubectl delete -f {} -n {}".format(self._work_path, "pv.yaml", self._namespace))

    def delete_pvc(self):
        os.system("cd {} && kubectl delete -f {} -n {}".format(self._work_path, "pvc.yaml", self._namespace))
        time.sleep(1)
        os.system("cd {} && kubectl delete -f {} -n {}".format(self._work_path, "pvc_pcd.yaml", self._namespace))
        time.sleep(1)
        os.system("cd {} && kubectl delete -f {} -n {}".format(self._work_path, "pvc_txt.yaml", self._namespace))
        time.sleep(1)
        os.system("cd {} && kubectl delete -f {} -n {}".format(self._work_path, "pvc_image.yaml", self._namespace))
        time.sleep(1)

    def run(self,namespace,restart=True):
        if not restart:
            self.init_name_space(namespace)
            self.init_pvc()
            self.init_server_first()
        else:
            self.init_name_space(namespace)
            self.init_pvc()
            self.init_server_not_first()



    def stop(self,namespace):
        self._namespace = namespace
        self.delete_name()
        self.delete_pvc()
        self.delete_server(namespace)








