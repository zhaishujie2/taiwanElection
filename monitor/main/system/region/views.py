# coding=utf-8
from flask import jsonify, request, url_for, send_from_directory, session

from monitor.main.system.region.region_infos import insert_area_info, delete_area_info, update_info_area, \
    select_area_info, select_area_info_one, select_area_info_page, insert_election_info, delete_election_info, \
    update_election_info, select_election_all, select_election_info_one, select_election_info_page, get_region_dict, \
    select_election_code_info, select_area_code_info
from . import mod
from monitor import app
import json, os
from monitor.util.mysql_util import closeAll


# 地区信息写入数据
@mod.route('/insert_area/',methods=['POST'])
def insert_area():
    try:
        datas = request.form.get('data', '')
        datas_info = json.loads(datas)
        administrative_id = datas_info.get('administrative_id')
        area_info = datas_info.get('area_info')
        governance_situation = datas_info.get('governance_situation')
        year = datas_info.get('year')

        if administrative_id and area_info and governance_situation and year:
            message = insert_area_info(administrative_id, area_info, governance_situation, year)
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400
        else:
            return jsonify({"message": "input info is not enough"}), 406

    except Exception as erro:
        app.logger.error(erro)
        return str(0)



# 地区信息删除数据
@mod.route('/delete_area/', methods=['POST'])
def delete_area():
    try:
        data = request.form.get('data', '')

        if data == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = delete_area_info(json.loads(data))
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400

    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 地区信息修改数据
@mod.route('/update_area/', methods=['POST'])
def update_area():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = update_info_area(json.loads(datas))
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400

    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 地区信息搜索所有数据
@mod.route('/select_area/',methods=['GET'])
def select_area():
    try:
        message, count = select_area_info()
        if message:
            return jsonify({"message": message, "count": count}), 200
        else:
            return jsonify({"message": "The data field is in the wrong", "count": count}), 400
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 地区信息根据id查询一条数据
@mod.route('/select_area_one/', methods=['POST'])
def select_area_one():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = select_area_info_one(json.loads(datas))
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 分页查询地区信息数据
@mod.route('/select_area_page/', methods=['POST'])
def select_area_page():
    try:
        datas = request.form.get('data', '')
        datas_info = json.loads(datas)
        page = datas_info['page']
        count = datas_info['count']

        if page and count:
            message = select_area_info_page(page, count)
            return jsonify({"message": message}), 200
        else:
            return jsonify({"message": "type input is null"}), 406
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 增加历届选举信息
@mod.route('/insert_election/', methods=['POST'])
def insert_election():
    try:
        datas = request.form.get('data', '')
        datas_info = json.loads(datas)
        administrative_id = datas_info.get('administrative_id')
        elector = datas_info.get('elector')
        election_score = datas_info.get('election_score')
        election_parties = datas_info.get('election_parties')
        period = datas_info.get('period')
        year = datas_info.get('year')

        if administrative_id and elector and election_score and election_parties and period and year:
            message = insert_election_info(administrative_id, elector, election_score, election_parties, period, year)
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400
        else:
            return jsonify({"message": "input info is not enough"}), 406

    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 删除历届选举信息
@mod.route('/delete_election/', methods=['POST'])
def delete_election():
    try:
        data = request.form.get('data', '')

        if data == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = delete_election_info(json.loads(data))
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400

    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 修改历届选举信息
@mod.route('/update_election/', methods=['POST'])
def update_election():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = update_election_info(json.loads(datas))
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400

    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 搜索全部历届选举信息
@mod.route('/select_election/',methods=['GET'])
def select_election():
    try:
        message, count = select_election_all()
        if message:
            return jsonify({"message": message, "count": count}), 200
        else:
            return jsonify({"message": "The data field is in the wrong", "count": count}), 400
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 根据id搜索一条选举信息
@mod.route('/select_election_one/', methods=['POST'])
def select_election_one():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = select_election_info_one(json.loads(datas))
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400

    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 分页查询历届选举信息
@mod.route('/select_election_page/', methods=['POST'])
def select_election_page():
    try:
        datas = request.form.get('data', '')
        datas_info = json.loads(datas)
        page = datas_info['page']
        count = datas_info['count']

        if page and count:
            message = select_election_info_page(page, count)
            return jsonify({"message": message}), 200
        else:
            return jsonify({"message": "type input is null"}), 406
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

# 根据地区信息编码查询数据
@mod.route('/select_area_code/', methods=['POST'])
def select_area_code():
    try:
        datas = request.form.get('data','')
        datas_info = json.loads(datas)
        administrative_id = datas_info['administrative_id']
        page = datas_info['page']
        count_info = datas_info['count']

        if administrative_id and page and count_info:
            message, count = select_area_code_info(administrative_id, page, count_info)
            if message:
                return jsonify({"message": message, "count": count}), 200
            else:
                return jsonify({"message": "The data field is in the wrong", "count": count}, ), 400
        else:
            return jsonify({"message": "type input is null"}), 406

    except Exception as erro:
        app.logger.error(erro)
        return str(0)

# 根据地区编号搜索选举信息
@mod.route('/select_election_code/', methods=['POST'])
def select_election_code():
    try:
        datas = request.form.get('data', '')
        datas_info = json.loads(datas)
        administrative_id = datas_info['administrative_id']
        page = datas_info['page']
        count_info = datas_info['count']

        if administrative_id and page and count_info:
            message, count = select_election_code_info(administrative_id, page, count_info)
            if message:
                return jsonify({"message": message, "count": count}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400
        else:
            return jsonify({"message": "type input is null"}), 406

    except Exception as erro:
        app.logger.error(erro)
        return str(0)

# 地区代码字典
@mod.route('/region_dict/', methods=['POST'])
def region_dict():
    try:
        data = request.form.get('data', '')
        if data == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            result = get_region_dict(json.loads(data))
            if result == None:
                return jsonify({"message": "The region field is in the wrong"}), 400
            else:
                return jsonify({"message": result}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)
