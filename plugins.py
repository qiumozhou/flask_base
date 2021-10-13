# -*- coding: utf-8 -*-
# @Time    : 2021/9/23 下午8:07
# @Author  : mozhouqiu
# @FileName: plugins.py
# @Email    ：15717163552@163.com
from flask import jsonify


def res_json(dict_data):
    if isinstance(dict_data,dict):
        return jsonify(dict_data)
    if len(dict_data) == 2:
        dict_data[0]["data"] = dict_data[1]
        return jsonify(dict_data[0])


def to_dict(obj):
    model_dict = dict(obj.__dict__)
    del model_dict['_sa_instance_state']
    return model_dict

def custom_field(field_list,dict_obj):
    data_dict={}
    for item in field_list:
        data_dict[item] = dict_obj.get(item,None)
    return data_dict
