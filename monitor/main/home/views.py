# coding=utf-8
from flask import request, session,jsonify
from monitor.main.home.show_party import get_party,get_everyinformation
from . import mod
import json

#画候选人团队
@mod.route('/team_infos/')
def get_all_information():
    message = {}
    try:
        message = session["electors"]
    except:
        return jsonify({"message":"session  is null"}),400
    result = get_party(message)
    if result ==0:
        return jsonify({"message":"The time field is in the wrong format"}),401
    return jsonify({"message":result})

#获取个人信息
@mod.route('/every_infos/',methods=['POST'])
def get_information():
    type = request.form.get('type','')
    name_id = request.form.get('id','')
    name = request.form.get('name','')
    department = request.form.get('department','')
    job = request.form.get('job','')
    content = {}
    if name == '' and department == '' and job == '':
        content['id'] = name_id
    elif name != '' and department != '' and job != '':
        content['id'] = name_id
        content['name'] = name
        content['department'] = department
        content['job'] = job
    # content = eval(request.form.get('content',''))
    if type == '' or type == None:
        return jsonify({"message":"输入类型"}),400
    elif content == '' or content == None:
        return jsonify({"message":"输入条件"}),400
    else:
        result,tag = get_everyinformation(type,content)
        if tag == '1':
            return jsonify({"message":result}),200
        if tag == '0':
            return jsonify({"message":result}),400

