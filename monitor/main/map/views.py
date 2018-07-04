# coding=utf-8
from flask import request, session, jsonify
from .draw_mysql import get_map_color, get_egional_electors,get_session,get_popularity_partisan
from .news_show import taiwan_latest_news, taiwan_event_news
from .election import get_popularity
from monitor import app
from monitor.util.utilclass import get_before_time
import datetime
from . import mod
import json


# 获取地图颜色信息
@mod.route('/get_map/')
def get_map():
    year = request.args.get('year', '')
    if year == None:
        app.logger.error("年份传入错误")
        return jsonify({"message": "年份传入错误"}), 406
    else:
        app.logger.info("获取" + year + "年的政党信息")
        result = get_map_color(int(year))
        if result == 0:
            return jsonify({"message": "年份传入错误"}), 406
        return jsonify({"message": result}), 200


@mod.route('/record_session/', methods=['POST'])
def record_session():
    data = request.form.get('data', '')
    dict = {}
    if data == '':
        return jsonify({"message": "data is null"}), 406
    else:
        try:
            data = json.loads(data)
            id = data["id"]
            year = data["year"]
            user_dict = get_egional_electors(int(id), int(year))
            if user_dict != 0:
                if len(user_dict) > 0:
                    session["electors"] = user_dict
                    session["year"] = year
                    session["area_id"] = id
                    img,partisan = get_session(int(id),int(year))
                    dict["electors"] =img
                    dict["partisan"] =partisan
                    dict["year"] = year
                    dict["area_id"] = id
                    return jsonify({"message": dict}), 200
                else:
                    return jsonify({"message": "传入的值在数据库中无法查出数据"}), 406
            else:
                return jsonify({"message": "传入的值在数据库中无法查出数据"}), 406
        except:
            return jsonify({"message": "传入area_id,year有误"}), 406


@mod.route('/get_latest_news/')
def get_latest_news():
    count = request.args.get('count', '')
    if count == '':
        app.logger.error("count传入错误")
        return jsonify({"message": "count传入错误"}), 406
    else:
        result = taiwan_latest_news(int(count))
        if result == 0:
            return jsonify({"message": "es查询出现错误"}), 406
        else:
            return jsonify({"message": result}), 200


@mod.route('/get_event_news/')
def get_event_news():
    count = request.args.get('count', '')
    if count == '':
        app.logger.error("count传入错误")
        return jsonify({"message": "count传入错误"}), 406
    else:
        result = taiwan_event_news(int(count))
        if result == 0:
            return jsonify({"message": "es查询出现错误"}), 406
        else:
            return jsonify({"message": result}), 200


@mod.route('/get_popularity/', methods=['POST'])
def get_popularity_info():
    data = request.form.get('data', '')
    dict = {}
    if data == '':
        return jsonify({"message": "data is null"}), 406
    try:
        data = json.loads(data)
        id = data["id"]
        year = data["year"]
        user_dict = get_egional_electors(int(id), int(year))
        if user_dict != 0:
            if len(user_dict) > 0:
                end_time = datetime.datetime.now().strftime("%Y-%m-%d")
                start_time = get_before_time(end_time, 45)
                result = get_popularity(start_time, end_time, user_dict)
                if result != 0:
                    return jsonify({"message": result}), 200
                else:
                    return jsonify({"message": "Support Rate Forecasting Problems"}), 406
            else:
                return jsonify({"message": "null"}), 200
        else:
            return jsonify({"message": "传入的值在数据库中无法查出数据"}), 406
    except:
        app.logger.error("传入area_id,year有误 id:", id, "year:", year)
        return jsonify({"message": "传入area_id,year有误"}), 406


@mod.route('/get_popularity_partisan/')
def get_popularity_partisan_info():
    result = get_popularity_partisan()
    if result == 0:
        return jsonify({"message": "mysql查询出现错误"}), 406
    else:
        return jsonify({"message": result}), 200