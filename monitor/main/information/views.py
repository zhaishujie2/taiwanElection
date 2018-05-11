# coding=utf-8
from flask import request, session, jsonify
from monitor import app
from . import mod
import json
from .information_statistics import get_information_facebook_statistics_count, get_information_news_statistics_count, \
    get_information_twitter_statistics_count, get_facebook_pages, get_all_facebook_pages, get_facebook_data, \
    get_all_facebook_data, get_news_pages, get_news_data, get_all_news_pages, get_all_news_data, get_twitter_pages, \
    get_twitter_data, get_all_twitter_pages, get_all_twitter_data


@mod.route('/get_facebook_statistics/', methods=['POST'])
def get_facebook_statistics():
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
        result = get_information_facebook_statistics_count(start_time, end_time, dict_name)
        if result == None:
            return jsonify({"message": "The time field is in the wrong format"}), 200
        else:
            return jsonify({"message": result}), 200


@mod.route('/get_news_statistics/', methods=['POST'])
def get_news_statistics():
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
        result = get_information_news_statistics_count(start_time, end_time, dict_name)
        if result == None:
            return jsonify({"message": "The time field is in the wrong format"}), 200
        else:
            return jsonify({"message": result}), 200


@mod.route('/get_twitter_statistics/', methods=['POST'])
def get_twitter_statistics():
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
        result = get_information_twitter_statistics_count(start_time, end_time, dict_name)
        if result == None:
            return jsonify({"message": "The time field is in the wrong format"}), 200
        else:
            return jsonify({"message": result}), 200


@mod.route('/facebook_pages/', methods=['POST'])
def get_facebook_count():
    data = request.form.get('data', '')
    start_time = ""
    end_time = ""
    name = ""
    if data == '':
        return jsonify({"message": "data input is null"}), 406
    else:
        try:
            data = json.loads(data)
            start_time = data["start_time"]
            end_time = data["end_time"]
            name = data["name"]
        except:
            return jsonify({"message": "start_time or end_time is error"}), 406
        result = get_facebook_pages(name, start_time, end_time)
        if result == None:
            return jsonify({"message": "The time field is in the wrong format"}), 200
        else:
            return jsonify({"message": result}), 200


@mod.route('/facebook_data/', methods=['POST'])
def facebook_data():
    data = request.form.get('data', '')
    page_number = 0
    page_size = 0
    start_time = ""
    end_time = ""
    name = ""
    if data == '':
        return jsonify({"message": "data input is null"}), 406
    else:
        try:
            data = json.loads(data)
            page_number = int(data["page_number"])
            page_size = int(data["page_size"])
            start_time = data["start_time"]
            end_time = data["end_time"]
            name = data["name"]
        except:
            return jsonify({"message": "input is error"}), 406
        result = get_facebook_data(name, page_number, page_size, start_time, end_time)
        if result == None:
            return jsonify({"message": "The time field is in the wrong format"}), 200
        else:
            return jsonify({"message": result}), 200


@mod.route('/facebook_all_pages/', methods=['POST'])
def get_all_facebook_count():
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
        result = get_all_facebook_pages(dict_name, start_time, end_time, )
        if result == None:
            return jsonify({"message": "The time field is in the wrong format"}), 200
        else:
            return jsonify({"message": result}), 200


@mod.route('/facebook_all_data/', methods=['POST'])
def facebook_data_all():
    data = request.form.get('data', '')
    page_number = 0
    page_size = 0
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
            page_number = data["page_number"]
            page_size = data["page_size"]
            start_time = data["start_time"]
            end_time = data["end_time"]
        except:
            return jsonify({"message": "input is error"}), 406
        result = get_all_facebook_data(dict_name, int(page_number), int(page_size), start_time, end_time)
        if result == None:
            return jsonify({"message": "The time field is in the wrong format"}), 200
        else:
            return jsonify({"message": result}), 200


@mod.route('/news_pages/', methods=['POST'])
def get_news_count():
    data = request.form.get('data', '')
    start_time = ""
    end_time = ""
    name = ""
    if data == '':
        return jsonify({"message": "data input is null"}), 406
    else:
        try:
            data = json.loads(data)
            start_time = data["start_time"]
            end_time = data["end_time"]
            name = data["name"]
        except:
            return jsonify({"message": "start_time or end_time or name is error"}), 406
        result = get_news_pages(name, start_time, end_time)
        if result == None:
            return jsonify({"message": "The time field is in the wrong format"}), 200
        else:
            return jsonify({"message": result}), 200


@mod.route('/news_data/', methods=['POST'])
def news_data():
    data = request.form.get('data', '')
    page_number = 0
    page_size = 0
    start_time = ""
    end_time = ""
    name = ""
    if data == '':
        return jsonify({"message": "data input is null"}), 406
    else:
        try:
            data = json.loads(data)
            page_number = int(data["page_number"])
            page_size = int(data["page_size"])
            start_time = data["start_time"]
            end_time = data["end_time"]
            name = data["name"]
        except:
            return jsonify({"message": "input is error"}), 406
        result = get_news_data(name, page_number, page_size, start_time, end_time)
        if result == None:
            return jsonify({"message": "The time field is in the wrong format"}), 200
        else:
            return jsonify({"message": result}), 200





@mod.route('/news_all_pages/', methods=['POST'])
def get_all_news_count():
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
        result = get_all_news_pages(dict_name, start_time, end_time, )
        if result == None:
            return jsonify({"message": "The time field is in the wrong format"}), 200
        else:
            return jsonify({"message": result}), 200


@mod.route('/news_all_data/', methods=['POST'])
def news_data_all():
    data = request.form.get('data', '')
    page_number = 0
    page_size = 0
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
            page_number = int(data["page_number"])
            page_size = int(data["page_size"])
            start_time = data["start_time"]
            end_time = data["end_time"]
        except:
            return jsonify({"message": "input is error"}), 406
        result = get_all_news_data(dict_name, page_number, page_size, start_time, end_time)
        if result == None:
            return jsonify({"message": "The time field is in the wrong format"}), 200
        else:
            return jsonify({"message": result}), 200


@mod.route('/twitter_pages/', methods=['POST'])
def get_twitter_count():
    data = request.form.get('data', '')
    start_time = ""
    end_time = ""
    name = ""
    if data == '':
        return jsonify({"message": "data input is null"}), 406
    else:
        try:
            data = json.loads(data)
            start_time = data["start_time"]
            end_time = data["end_time"]
            name = data["name"]
        except:
            return jsonify({"message": "start_time or end_time is error"}), 406
        result = get_twitter_pages(name, start_time, end_time)
        if result == None:
            return jsonify({"message": "The time field is in the wrong format"}), 200
        else:
            return jsonify({"message": result}), 200


@mod.route('/twitter_data/', methods=['POST'])
def twitter_data():
    data = request.form.get('data', '')
    page_number = 0
    page_size = 0
    start_time = ""
    end_time = ""
    name = ""
    if data == '':
        return jsonify({"message": "data input is null"}), 406
    else:
        try:
            data = json.loads(data)
            page_number = int(data["page_number"])
            page_size = int(data["page_size"])
            start_time = data["start_time"]
            end_time = data["end_time"]
            name = data["name"]
        except:
            return jsonify({"message": "input is error"}), 406
        result = get_twitter_data(name, page_number, page_size, start_time, end_time)
        if result == None:
            return jsonify({"message": "The time field is in the wrong format"}), 200
        else:
            return jsonify({"message": result}), 200


@mod.route('/twitter_all_pages/', methods=['POST'])
def get_all_twitter_count():
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
        result = get_all_twitter_pages(dict_name, start_time, end_time, )
        if result == None:
            return jsonify({"message": "The time field is in the wrong format"}), 200
        else:
            return jsonify({"message": result}), 200


@mod.route('/twitter_all_data/', methods=['POST'])
def twitter_data_all():
    data = request.form.get('data', '')
    page_number = 0
    page_size = 0
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
            page_number = int(data["page_number"])
            page_size = int(data["page_size"])
            start_time = data["start_time"]
            end_time = data["end_time"]
        except:
            return jsonify({"message": "input is error"}), 406
        result = get_all_twitter_data(dict_name, page_number, page_size, start_time, end_time)
        if result == None:
            return jsonify({"message": "The time field is in the wrong format"}), 200
        else:
            return jsonify({"message": result}), 200
