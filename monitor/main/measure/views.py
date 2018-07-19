# coding=utf-8
from flask import jsonify, request, url_for, send_from_directory, session
from . import mod
from monitor import app
from monitor.util.config import upload_files
from monitor.main.measure.measure_operate import allowed_file, save_new_file, process_delete, select_file_all, \
    insert_message_info, select_messages, \
    delete_messages, delete_user_info, login, add_new_user, select_users_all, update_users_info, select_user_info_one, \
    select_user_info_page, update_file_label, select_message_info_page
import json, os


# 上传文件
@mod.route('/upload_word/', methods=['post'])
def upload_word():
    try:
        # user_name = request.form.get('user_name', '')
        user_name = session.get("user")

        is_private = request.form.get('is_private', '')
        file_label = request.form.get('file_label', '')
        if user_name and is_private:
            f = request.files['file']
            if f and allowed_file(f.filename):
                doc_name = f.filename
                f.save(os.path.join(upload_files, doc_name))
                file_root = os.path.join(upload_files, doc_name)
                message = save_new_file(file_root, doc_name, user_name, is_private, file_label)
                if message:
                    return jsonify({"message": message}), 201
            else:
                return jsonify({"message": "文档未存储成功"}), 400
        else:
            return jsonify({"message": "input is null"}), 406

    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 下载文件
@mod.route("/download/<path:filename>")
def downloader(filename):
    try:
        dirpath = os.path.join(upload_files)  # 这里是下载目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
        return send_from_directory(dirpath, filename, as_attachment=True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 删除文件
@mod.route("/remove_file/", methods=['post'])
def remove_file():
    try:
        file_name = request.form.get('file_name', '')
        user_name = session.get('user')
        print(file_name, user_name)
        if file_name and user_name:
            message = process_delete(file_name, user_name)
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "0"}), 406
        else:
            return jsonify({"message": "input is null"}), 406
    except Exception as erro:
        app.logger.error(erro)
        return str(3)


# 修改或者删除文档的标签
@mod.route("/update_label/", methods=['post'])
def update_label():
    try:
        datas = request.form.get('data', '')
        datas_info = json.loads(datas)
        if datas_info:
            message = update_file_label(datas_info)
            return jsonify({"message": message}), 200
        else:
            return jsonify({"message": "input is null"}), 406
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 显示该用户能看到的所有文件
@mod.route("/select_file/", methods=['post'])
def select_file():
    try:
        user_name = session.get('user')
        print(user_name)
        if user_name:
            message = select_file_all(user_name)
            return jsonify({"message": message}), 200
        else:
            return jsonify({"message": "input is null"}), 406
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 用户反馈消息插入
@mod.route("/insert_message/", methods=['post'])
def insert_message():
    try:
        datas = request.form.get('data', '')
        datas_info = json.loads(datas)
        user_name = session.get('user')
        model_info = datas_info.get('model_info')
        message = datas_info.get('message')
        if model_info and message:
            message = insert_message_info(user_name, model_info, message)
            return jsonify({"message": message}), 200
        else:
            return jsonify({"message": "input is null"}), 406

    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 查看所有消息
@mod.route("/select_message/", methods=['post'])
def select_message():
    try:
        user_name = session.get('user')
        if user_name:
            message, count = select_messages()
            return jsonify({"message": message, "all_count": count}), 200
        else:
            return jsonify({"message": "input is null"}), 406
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 分页查询留言信息
@mod.route('/select_message_page/', methods=['POST'])
def select_message_page():
    try:
        datas = request.form.get('data', '')
        datas_info = json.loads(datas)
        page = datas_info['page']
        count = datas_info['count']

        if page and count:
            message = select_message_info_page(page, count)
            return jsonify({"message": message}), 200
        else:
            return jsonify({"message": "type input is null"}), 406
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 删除消息
@mod.route("/delete_message/", methods=['post'])
def delete_message():
    try:
        datas = request.form.get('data', '')
        datas_info = json.loads(datas)
        user_name = session.get('user')
        message_id = datas_info.get('messages_id')
        if user_name and message_id:
            message = delete_messages(user_name, message_id)
            return jsonify({"message": message}), 200
        else:
            return jsonify({"message": "input is null"}), 406
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 用户登录界面
@mod.route('/login/', methods=['POST'])
def login_user():
    user = request.form.get('user', '')
    password = request.form.get('password', '')
    if user == '' or password == '':
        return jsonify({"message": "user or password is null"}), 406
    else:
        result, info = login(user, password)
        if result != 0:
            try:
                session["user"] = user
                session["user_level"] = info
                print('================')
                print(session.get('user'))
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
    if user == None and user_level == None:
        app.logger.info("user and user level in null")
        return jsonify({"message": "user and user_level is null"}), 406
    else:
        app.logger.info("获取user:" + user)
        return jsonify({"user": user, "user_level": user_level}), 200


# 注销

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


# 添加用户，超级管理员添加管理员，管理员添加普通用户，普通用户不可以添加
@mod.route('/insert_user/', methods=['POST'])
def insert_user():
    try:
        datas = request.form.get('data', '')
        data = json.loads(datas)
        new_user = data.get('new_user')
        password = data.get('password')
        user_level = data.get('user_level')
        user_level = str(user_level)
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
