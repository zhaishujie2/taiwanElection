# coding=utf-8
from flask import request, session,jsonify
from .show_party import get_party,get_everyinformation,get_gov_area,get_all_candidate_infos
from . import mod
import json
from .election import get_popularity

#画候选人团队
@mod.route('/team_infos/')
def get_all_information():
    message = {}
    try:
        message = session["electors"]
    except:
        return jsonify({"message":"session  is null"}),401
    result = get_party(message)
    if result == 0:
        return jsonify({"message":"The time field is in the wrong format"}),401
    return jsonify({"message":result})

#获取个人信息
@mod.route('/every_infos/',methods=['POST'])
def get_information():
    type = request.form.get('type','')
    content = eval(request.form.get('content',''))
    if type == '' or type == None:
        return jsonify({"message":"输入类型"}),400
    elif content == '' or content == None:
        return jsonify({"message":"输入条件"}),400
    else:
        result = get_everyinformation(type,content)
        if result == 0:
            return jsonify({"message":"The time field is in the wrong format"}),401
        return jsonify({"message":result})

#获取地区基本信息
@mod.route('/gov_area/')
def gov_area():
    message = {}
    try:
        year = session["year"]
        id = session["area_id"]
    except:
        return jsonify({"message":"session  is null"}),401
    result = get_gov_area(id,year)
    if result == 0:
        return jsonify({"message":"The time field is in the wrong format"}),401
    return jsonify({"message":result})





#获取当前支持率
@mod.route('/get_popularity/',methods=['POST'])
def get_popularity_statistics():
    data = request.form.get('data', '')
    start_time = ""
    end_time = ""
    dict_name = {}
    if data == '':
        return jsonify({"message": "data input is null"}), 406
    else:
        try:
            dict_name = session["electors"]
        except:
            return jsonify({"message": "session  is null"}), 401
        try:
            data = json.loads(data)
            start_time = data["start_time"]
            end_time = data["end_time"]
        except:
            return jsonify({"message": "start_time or end_time is error"}), 406
        result = get_popularity(start_time, end_time, dict_name)
        if result == 0:
            return jsonify({"message": "The time field is in the wrong format"}), 200
        else:
            return jsonify({"message": result}), 200

#获取历届选举信息
@mod.route('/candidate_infos/')
def get_candidate_infos():
    year = 0
    id = 0
    dict_name = {}
    try:
        year = int(session["year"])
        id = int(session["area_id"])
    except:
        return jsonify({"message": "session  is null"}), 401
    result = get_all_candidate_infos(id, year)
    if result == 0:
        return jsonify({"message": "The time field is in the wrong format"}), 402
    else:
        return jsonify({"message": result}), 200