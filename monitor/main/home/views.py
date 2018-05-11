# coding=utf-8
from flask import request, session,jsonify
from monitor.main.home.show_info import get_popular_info
from . import mod
import json

#获取支持趋势
@mod.route('/get_popular')
def get_all_popular():
    date = request.args.get('date','')
    message = json.loads(session["electors"])
    print(date)
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

