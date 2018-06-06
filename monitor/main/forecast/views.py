# coding=utf-8
from flask import request, session, jsonify
from monitor import app
from . import mod
import json
from .information import get_google_trend,get_facebook_trend,get_popular_info,get_current_support_info,get_year_support_info


@mod.route('/get_google_trend/', methods=['POST'])
def get_google_trend_info():
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
        result = get_google_trend(start_time, end_time, dict_name)
        if result == 0:
            return jsonify({"message": "The time field is in the wrong format"}), 200
        else:
            return jsonify({"message": result}), 200

@mod.route('/get_facebook_trend/', methods=['POST'])
def get_facebook_trend_info():
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
        result = get_facebook_trend(start_time, end_time, dict_name)
        if result == 0:
            return jsonify({"message": "The time field is in the wrong format"}), 401
        else:
            return jsonify({"message": result}), 200




@mod.route('/get_popular/', methods=['POST'])
def get_popular_trend_info():
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
        result = get_popular_info(start_time, end_time, dict_name)
        if result == 0:
            return jsonify({"message": "The time field is in the wrong format"}), 403
        else:
            return jsonify({"message": result}), 200

@mod.route('/get_current_support/')
def get_current_support():
    dict_name = {}
    year = 0
    try:
        dict_name = session["electors"]
        year = session["year"]
    except:
        return jsonify({"message": "session  is null"}), 401
    result = get_current_support_info(year, dict_name)
    if result == 0:
        return jsonify({"message": "The time field is in the wrong format"}), 403
    else:
        return jsonify({"message": result}), 200


@mod.route('/get_year_support/')
def get_year_support():
    dict_name = {}
    year = 0
    try:
        dict_name = session["electors"]
        year = session["year"]
    except:
        return jsonify({"message": "session  is null"}), 401
    result = get_year_support_info(year, dict_name)
    if result == 0:
        return jsonify({"message": "The time field is in the wrong format"}), 403
    else:
        return jsonify({"message": result}), 200