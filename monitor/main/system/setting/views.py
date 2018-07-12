# coding=utf-8
from flask import jsonify, request, url_for, send_from_directory, session

from monitor.main.system.setting.setting_infos import login, add_new_user, delete_user_info, update_users_info, \
    select_users_all, select_user_info_one, select_user_info_page
from . import mod
from monitor import app
import json, os
from monitor.util.mysql_util import closeAll


# 获取当前用户ip
@mod.route('/get_ip/', methods=['GET'])
def get_ip():
    ip = request.remote_addr
    if ip:
        return jsonify({"message": ip}), 200
    else:
        return jsonify({"message": "The ip is null"}), 400


@mod.route('/login/', methods=['POST'])
def login_user():
    user = request.form.get('user', '')
    password = request.form.get('password', '')
    if user == '' or password == '':
        return jsonify({"message": "user or password is null"}), 406
    else:
        result, info = login(user, password)
        print(info)
        if result != 0:
            try:
                session["user"] = user
                session["user_level"] = info
                return jsonify({"message": "ok", "user_level": info}), 200
            except (Exception)as e:
                app.logger.error(e)
                return jsonify({"message": "session update error"}), 406
        else:
            return jsonify({"message": "username or password is incorrect"}), 401


# 获得登陆用户名
@mod.route('/get_session/')
def get_sessions():
    user = session.get("user")
    user_level = session.get("user_level")
    print(user, user_level)
    if user == None and user_level == None:
        app.logger.info("user and user level in null")
        return jsonify({"message": "user and user_level is null"}), 406
    else:
        app.logger.info("获取user:" + user)
        return jsonify({"user": user, "user_level": user_level}), 200


@mod.route('/logout/')
def del_session():
    app.logger.info("用户注销数据！")
    user = session.get("user")
    user_level = session.get("user_level")
    if user == None and user_level == None:
        return jsonify({"message": "注销成功"}), 200
    else:
        session.pop("user")
        session.pop("user_level")
        user = session.get("user")
        user_level = session.get("user_level")
        if user == None and user_level == None:
            return jsonify({"message": "注销成功"}), 200
        else:
            return jsonify({"message": "注销失败"}), 406



@mod.route('/insert_user/', methods=['POST'])
def insert_user():
    try:
        datas = request.form.get('data', '')
        data = json.loads(datas)
        new_user = data.get('new_user')
        password = data.get('password')
        user_level = data.get('user_level')
        user_level = str(user_level)
        print(new_user, password, user_level)
        if new_user and password and user_level:
            message = add_new_user(new_user, password, user_level)
            return jsonify({"message": message}), 200
        else:
            return jsonify({"message": "new_user or password or user_level is null"}), 406

    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 删除用户
@mod.route('/delete_user/', methods=['POST'])
def delete_user():
    try:
        data = request.form.get('data', '')

        if data == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = delete_user_info(json.loads(data))
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400

    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 修改用户信息
@mod.route('/update_users/', methods=['POST'])
def update_users():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = update_users_info(json.loads(datas))
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400

    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 查看所有用户
@mod.route('/select_users/', methods=['GET'])
def select_users():
    try:
        message, count = select_users_all()
        if message:
            return jsonify({"message": message, "count": count}), 200
        else:
            return jsonify({"message": "The data field is in the wrong", "count": count}), 400
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 获取单个用户
@mod.route('/select_user_one/', methods=['post'])
def select_user_one():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = select_user_info_one(json.loads(datas))
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


@mod.route('/select_user_page/', methods=['POST'])
def select_user_page():
    try:
        datas = request.form.get('data', '')
        datas_info = json.loads(datas)
        page = datas_info['page']
        count = datas_info['count']

        if page and count:
            message = select_user_info_page(page, count)
            return jsonify({"message": message}), 200
        else:
            return jsonify({"message": "type input is null"}), 406
    except Exception as erro:
        app.logger.error(erro)
        return str(0)