# coding=utf-8
from flask import request, session,jsonify
from monitor.main.home.show_info import get_popular_info
from monitor.main.home.show_party import get_party,get_everyinformation
from . import mod
import json

#获取支持趋势
@mod.route('/get_popular')
def get_all_popular():
    date = request.args.get('date','')
    message = json.loads(session["electors"])
    # print(date)
    if len(date) == 2:
        return jsonify({"message":"请输入日期"}),400
    else:
        result,num = get_popular_info(date,message)
        if num is '1':
            return jsonify(result),200
        elif num is '0':
            return jsonify({"message":"此日期内无数据"}),400
        else:
            return jsonify({"message":result}),400


#画候选人团队
@mod.route('/team_infos')
def get_all_information():
    message = json.loads(session["electors"])
    if len(session["electors"]) == 0 or message == None:
        return jsonify({"message":"session  is null"})
    else:
        result = get_party(message)
    return jsonify({"message":result})

#获取个人信息
@mod.route('/every_infos',methods=['POST'])
def get_information():
    type = request.form.get('type','')
    content = eval(request.form.get('content',''))
    if type == '' or type == None:
        return jsonify({"message":"输入类型"})
    elif content == '' or content == None:
        return jsonify({"message":"输入条件"})
    else:
        result = get_everyinformation(type,content)
        return jsonify({"message":result})

