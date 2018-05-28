# coding=utf-8
from flask import jsonify,request
from . import mod
from monitor import app
from monitor.main.system.operate_info import insert_info,delete_info,update_info,select_info,get_is_candidate,get_region_dict,get_one_infos
import json

#写入数据
@mod.route('/insert/',methods=['POST'])
def insert():
    datas = request.form.get('data','')
    if len(datas) == 2:
        return jsonify({"message":"请输入信息"}),400
    else:
        message = insert_info(json.loads(datas))
        if message is '1':
            return jsonify({"message" : "ok"}),201
        else:
            return jsonify({"message":message}),400

#删除数据
@mod.route('/delete/',methods=['POST'])
def delete():
    data = request.form.get('data','')
    if data == '':
        return  jsonify({"message":"请输入需要删除的数据"})
    else:
        message = delete_info(json.loads(data))
        if message is '1':
            return jsonify({"message" : "数据删除成功"}),201
        else:
            return jsonify({"message" : "没有数据删除"}),400

#修改数据
@mod.route('/update/',methods=['POST'])
def update():
    datas = request.form.get('data','')
    if datas == '':
        return  jsonify({"message":"请输入需要修改的信息"})
    else:
        message = update_info(json.loads(datas))
    if message is '1':
        return jsonify({"message":"数据更新成功"}),201
    else:
        return jsonify({"message":message}),400


#查询数据
@mod.route('/select/',methods=['POST'])
def select():
    datas = request.form.get('data','')
    if datas == '':
        return  jsonify({"message":"请输入需要查询的信息"})
    else:
        message,tag = select_info(json.loads(datas))
    if tag is '1':
        return jsonify({"message":message}),200
    elif tag is '0':
        return jsonify({"message":"根据此条件无信息"}),401
    else:
        return jsonify({"message":message}),400


#查询候选人是否存在
#返回0 表示无，返回1 表示有，返回大于1 表示有重复数据，返回406表示输入的地区代码有错
@mod.route('/is_candidate/',methods=['POST'])
def is_candidate():
    try:
        datas = request.form.get('data','')
        if len(datas) < 3 or datas == '':
            return jsonify({"message": "data input is wrong"}), 406
        else:
            result = get_is_candidate(json.loads(datas))
            if result == None:
                return jsonify({"message": "The data field is in the wrong"}), 200
            else:
                return jsonify({"message": result}),200
    except Exception as erro:
        app.logger.error(erro)
        return 0

#根据id查询单条信息
@mod.route('/one_select/',methods=['POST'])
def one_info():
    try:
        datas = request.form.get('data','')
        data = json.loads(datas)
        info_type = data.get('type')
        if info_type == '':
            return jsonify({"message": "type input is null"}), 406
        if data == '':
            return jsonify({"message": "data input is null"}), 406
        else:
            result = get_one_infos(info_type,data)
            if result == None:
                return jsonify({"message": "The data is wrong"}), 400
            else:
                return jsonify({"message": result}),200
    except Exception as erro:
        app.logger.error(erro)
        return 0

#地区代码字典
@mod.route('/region_dict/',methods = ['POST'])
def region_dict():
    # try:
        data = request.form.get('data','')
        if data == '':
            return jsonify({"message": "type input is null"}),406
        else:
            result = get_region_dict(json.loads(data))
            if result == None:
                return jsonify({"message": "The region field is in the wrong"}), 200
            else:
                return jsonify({"message": result}),200
    # except Exception as erro:
    #     app.logger.error(erro)
    #     return str(0)