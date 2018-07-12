# coding=utf-8
from flask import jsonify, request,session

from monitor.main.system.support.support_infos import select_support, delete_support, update_support, insert_support, \
    select_partisan, delete_partisan, update_partisan, insert_partisan, get_pages, get_all_years, get_region_dict
from . import mod
from monitor import app
import json


#获取民调数据
@mod.route('/select_support/',methods=['POST'])
def sele_support():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = select_support(json.loads(datas))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": message}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

#删除民调数据
@mod.route('/delete_support/',methods=['POST'])
def dele_support():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = delete_support(json.loads(datas))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": message}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

#修改民调数据
@mod.route('/update_support/',methods=['POST'])
def upda_support():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = update_support(json.loads(datas))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": message}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

#添加民调数据
@mod.route('/insert_support/',methods=['POST'])
def inse_support():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = insert_support(json.loads(datas))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": message}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


#获取党派数据
@mod.route('/select_partisan/',methods=['POST'])
def sele_partisan():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = select_partisan(json.loads(datas))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": message}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

#删除党派数据
@mod.route('/delete_partisan/',methods=['POST'])
def dele_partisan():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = delete_partisan(json.loads(datas))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": message}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

#修改党派数据
@mod.route('/update_partisan/',methods=['POST'])
def upda_partisan():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = update_partisan(json.loads(datas))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": message}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

#添加党派数据
@mod.route('/insert_partisan/',methods=['POST'])
def inse_partisan():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = insert_partisan(json.loads(datas))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": message}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

# 做分页
@mod.route('/pages/', methods=['POST'])
def pages():
    try:
        data = request.form.get('data','')
        datas = json.loads(data)
        result = get_pages(datas)
        if result == 0:
            return jsonify({"message": "The data is wrong "}), 400
        return jsonify({"message": result}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

# 根据地区返回该地区的所有年份
@mod.route('/years_candidates/', methods=['POST'])
def years():
    try:
        datas = request.form.get('data', '')
        if datas == '' or datas == None:
            return jsonify({"message": "data input is null"}), 406
        else:
            data = json.loads(datas)
            info_type = data.get('type')
            result = get_all_years(info_type, data)
            if result == 0:
                return jsonify({"message": "The data is wrong "}), 400
            return jsonify({"message": result}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

# 获得登陆用户名
@mod.route('/get_session/')
def get_sessions():
    user = session.get("user")
    user_level = session.get("user_level")
    print(user, user_level)
    if user == None and user_level == None:
        app.logger.info("user and user level in null")
        return jsonify({"message": "user and user_level is null"}), 406
    else:
        app.logger.info("获取user:" + user)
        return jsonify({"user": user, "user_level": user_level}), 200

# 地区代码字典
@mod.route('/region_dict/', methods=['POST'])
def region_dict():
    try:
        data = request.form.get('data', '')
        if data == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            result = get_region_dict(json.loads(data))
            if result == None:
                return jsonify({"message": "The region field is in the wrong"}), 400
            else:
                return jsonify({"message": result}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)
