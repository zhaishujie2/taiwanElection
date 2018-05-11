# coding=utf-8
from flask import jsonify,request
from . import mod
from monitor.main.system.operate_info import insert_info,delete_info,update_info,select_info
import json

#写入数据
@mod.route('/insert',methods=['POST'])
def insert():
    datas = request.form.get('data','')
    if len(datas) == 2:
        return jsonify({"message":"请输入信息"}),400
    else:
        message = insert_info(json.loads(datas))
        if message is '1':
            return jsonify({"message" : "ok"}),201
        elif message is '0':
            return jsonify({"message" : "未有数据写入"}),400
        else:
            return jsonify({"message":message}),400

#删除数据
@mod.route('/delete',methods=['POST'])
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
@mod.route('/update',methods=['POST'])
def update():
    datas = request.form.get('data','')
    if datas == '':
        return  jsonify({"message":"请输入需要修改的信息"})
    else:
        message = update_info(json.loads(datas))
    if message is '1':
        return jsonify({"message":"数据更新成功"}),201
    elif message is '0':
        return jsonify({"message":"数据未更新"}),401
    else:
        return jsonify({"message":message}),400


#查询数据
@mod.route('/select',methods=['POST'])
def select():
    datas = request.form.get('data','')
    if datas == '':
        return  jsonify({"message":"请输入需要查询的信息"})
    else:
        message = select_info(json.loads(datas))
    if message is '1':
        return jsonify({"message":message}),201
    elif message is '0':
        return jsonify({"message":"根据此条件无信息"}),401
    else:
        return jsonify({"message":message}),400
