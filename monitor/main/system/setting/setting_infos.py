# coding=utf-8
from monitor.main.system.util import get_date_item
from monitor.util.mysql_util import getconn, closeAll, md5
from monitor import app
import os,sys

# 登录界面
def login(name, password):
    conn = getconn()
    cur = conn.cursor()
    try:
        password = md5(password)
        sql = "select `user`, `position` from users where user=%s and passwd=%s"
        result = cur.execute(sql, (name, password))
        if result < 1:

            return 0, 0
        else:
            info = cur.fetchone()
            return result, info[1]

    except (Exception) as e:
        app.logger.error(e)
        return "0"
    finally:
        closeAll(conn,cur)


# 插入用户
def add_new_user(new_user,password, user_level):
    conn = getconn()
    cur = conn.cursor()
    try:
        insert_sql = """INSERT INTO `users` (`user`,`passwd`,`position`) VALUES (%s,%s,%s)"""
        select_sql = """SELECT `user` FROM `users` WHERE `user`= %s"""
        select_result = cur.execute(select_sql, new_user)
        if select_result != 0:
            return "当前用户已存在"
        password = md5(password)
        result = cur.execute(insert_sql, (new_user, password, user_level))
        if result < 1:
            return "插入失败"
        else:
            return "插入成功"
    except (Exception) as e:
        app.logger.error(e)
        return "0"
    finally:
        closeAll(conn, cur)


# 删除用户
def delete_user_info(data):
    conn = getconn()
    cur = conn.cursor()
    id = data.get('id')
    try:
        delete_sql = """DELETE FROM `users` WHERE id = %s """
        re = cur.execute(delete_sql, id)
        if re < 1:
            return 0
        else:
            return 1
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 查单个用户的密码
def select_user_secret(id):
    conn = getconn()
    cur = conn.cursor()
    try:
        select_sql = """SELECT `passwd` FROM `users` WHERE `id` = %s """
        re = cur.execute(select_sql, id)
        if re < 1:
            return 0
        else:
            item = cur.fetchone()
            # print(item)
            pass_word = item[0]
            return pass_word
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 修改用户信息
def update_users_info(datas):
    where_dict = datas.get('where_dict')
    up_dict = datas.get('up_dict')
    if len(where_dict) == 0 or len(up_dict) == 0:
        if len(where_dict) == 0:
            return "更新条件不能为空"
        if len(up_dict) == 0:
            return "更新内容不能为空"
    else:
        conn = getconn()
        cur = conn.cursor()
        try:
            where_sql = ''
            up_sql = ''
            where_num = 0
            up_num = 0
            for k, v in where_dict.items():
                ency_password = select_user_secret(v)
                print(ency_password)
                where_num += 1
                if where_num < len(where_dict):
                    where_sql += "{} = '{}' AND ".format(k, v)
                else:
                    where_sql += "{} = '{}'".format(k, v)
            for k, v in up_dict.items():
                if k == "passwd":
                    if v:
                        v = md5(v)
                    else:
                        v = ency_password
                up_num += 1
                if up_num < len(up_dict):
                    up_sql += "{} = '{}', ".format(k, v)
                else:
                    up_sql += "{} = '{}' ".format(k, v)
            update_sql = """UPDATE `users` SET """ + up_sql + ' WHERE ' + where_sql
            re = cur.execute(update_sql)
            if re < 1:
                return 0
            else:
                return 1
        except Exception as erro:
            app.logger.error(erro)
            return 0
        finally:
            closeAll(conn, cur)


# 查询所有用户信息
def select_users_all():
    conn = getconn()
    cur = conn.cursor()

    try:
        select_sql = """SELECT `id`,`user` ,`position` FROM `users` """
        re = cur.execute(select_sql)
        if re < 1:
            return 0, 0
        else:
            count = re
            result = cur.fetchall()
            lists = []
            for item in result:
                dict = {}
                dict['id'] = item[0]
                dict['user'] = item[1]
                dict['position'] = item[2]
                lists.append(dict)
            return lists, count
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn,cur)


# 获取一条用户数据
def select_user_info_one(data):
    conn = getconn()
    cur = conn.cursor()
    id = data['id']
    try:
        select_sql = """SELECT `user`,`position`  FROM `users` WHERE `id` = %s """
        re = cur.execute(select_sql, id)
        if re < 1:
            return 0
        else:
            item = cur.fetchone()
            dict = {}

            dict['user_name'] = item[0]
            dict['position'] = item[1]
            return dict
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 分页获取用户数据
def select_user_info_page(page, count):
    conn = getconn()
    cur = conn.cursor()
    try:
        select_info = '''SELECT `id`,`user`,`position` FROM `users` LIMIT %s, %s;'''
        count = count
        if int(page) == 1 or int(page) == 0:
            page_t = 0
        else:
            page_t = (int(page) - 1) * int(count)
        re = cur.execute(select_info, (int(page_t), int(count)))
        if re < 1:
            return 0
        else:
            result = cur.fetchall()
            lists = []
            for item in result:
                dict = {}
                dict['id'] = item[0]
                dict['user'] = item[1]
                dict['position'] = item[2]
                lists.append(dict)
            return lists
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)