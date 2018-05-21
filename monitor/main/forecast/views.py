# coding=utf-8
from flask import request, session, jsonify
from monitor import app
from . import mod
import json
from .information import get_google_trend


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
            print (start_time,end_time)
        except:
            return jsonify({"message": "start_time or end_time is error"}), 406
        result = get_google_trend(start_time, end_time, dict_name)
        if result == None:
            return jsonify({"message": "The time field is in the wrong format"}), 200
        else:
            return jsonify({"message": result}), 200



