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
    result = get_popular_info(date,message)
    return jsonify(result)

