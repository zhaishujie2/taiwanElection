# coding=utf-8
from flask import request, session, jsonify
from .show_party import get_party, get_everyinformation, get_gov_area, get_all_candidate_infos
from . import mod
from monitor import app
import json
from .election import get_popularity


# 画候选人团队
@mod.route('/team_infos/')
def get_all_information():
    message = {}
    try:
        message = session["electors"]
    except:
        return jsonify({"message": "session  is null"}), 406
    result = get_party(message)
    if result == 0:
        return jsonify({"message": "The data is in wrong"}), 401
    return jsonify({"message": result}), 200


# 获取个人信息
@mod.route('/every_infos/', methods=['POST'])
def get_information():
    try:
        datas = request.form.get('data', '')
        data = json.loads(datas)
        info_type = data.get('type')
        content = data.get('content')
        if info_type == '' or info_type == None:
            return jsonify({"message": "type input is null"}), 406
        elif content == '' or content == None:
            return jsonify({"message": "data input is null"}), 406
        else:
            result = get_everyinformation(info_type, content)
            if result == 0:
                return jsonify({"message": "The data is wrong "}), 400
            return jsonify({"message": result}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)



# 获取地区基本信息
@mod.route('/gov_area/')
def gov_area():
    message = {}
    try:
        year = session["year"]
        id = session["area_id"]
    except:
        return jsonify({"message": "session  is null"}), 401
    result = get_gov_area(id, year)
    if result == 0:
        return jsonify({"message": "The time field is in the wrong format"}), 401
    return jsonify({"message": result}), 200


# 获取当前支持率
@mod.route('/get_popularity/', methods=['POST'])
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


# 获取历届选举信息
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
