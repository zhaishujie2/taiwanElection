# coding=utf-8
from flask import request, session
from .draw_mysql import login
from monitor import app
from . import mod


# 用户登录界面
@mod.route('/login/', methods=['POST'])
def login_user():
    user = request.form.get('user', '')
    password = request.form.get('password', '')
    if user == '' or password == '':
        print("user or password is null")
        return '0'
    else:
        result = login(user, password)
        if result != 0:
            try:
                session["user"] = user
                return "1"
            except (Exception )as e:
                app.logger.error(e)
                return "0"
        else:
            return "0"


# 获得登陆用户名
@mod.route('/get_session/')
def get_sessions():
    user = session.get("user")
    if user == None:
        app.logger.info("没有用户登陆")
        return "0"
    else:
        app.logger.info("获取user:"+user)
        return user


# 注销

@mod.route('/logout/')
def del_session():
    app.logger.info("用户注销数据！")
    user = session.get("user")
    if user == None:
        return "1"
    else:
        session.pop("user")
        user = session.get("user")
        if user == None:
            return "1"
        else:
            return "0"
