# coding=utf-8
from flask import request, session, jsonify
from .draw_mysql import login
from monitor import app
from . import mod


# 用户登录界面
@mod.route('/login/', methods=['POST'])
def login_user():
    user = request.form.get('user', '')
    password = request.form.get('password', '')
    if user == '' or password == '':
        return jsonify({"message": "user or password is null"}), 406
    else:
        result = login(user, password)
        if result != 0:
            try:
                session["user"] = user
                return jsonify({"message": "ok"}), 200
            except (Exception)as e:
                app.logger.error(e)
                return jsonify({"message": "session update error"}), 406
        else:
            return jsonify({"message": "username or password is incorrect"}), 401


# 获得登陆用户名
@mod.route('/get_session/')
def get_sessions():
    user = session.get("user")
    if user == None:
        app.logger.info("user in null")
        return jsonify({"message": "user is null"}), 406
    else:
        app.logger.info("获取user:" + user)
        return jsonify({"message": user}), 200


# 注销

@mod.route('/logout/')
def del_session():
    app.logger.info("用户注销数据！")
    user = session.get("user")
    if user == None:
        return jsonify({"message": "注销成功"}), 200
    else:
        session.pop("user")
        user = session.get("user")
        if user == None:
            return jsonify({"message": "注销成功"}), 200
        else:
            return jsonify({"message": "注销失败"}), 406
