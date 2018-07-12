# coding=utf-8
from monitor.main.system.util import get_date_item
from monitor.util.mysql_util import getconn, closeAll, md5
from monitor import app
import os,sys



# 地区代码
def get_region_dict(data):
    name = data.get('name')
    id = data.get('id')
    every = data.get('every')
    conn = getconn()
    cur = conn.cursor()
    if len(data) == 1 and name != None:
        select_sql = """SELECT `administrative_id` FROM `administrative_area` WHERE `administrative_name` = %s"""
        try:
            cur.execute(select_sql, (name))
            name_re = cur.fetchone()
        except Exception as erro:
            app.logger.error(erro)
            return 0
        finally:
            closeAll(conn, cur)
        if name_re != '' or name_re != None:
            return name_re[0]
        else:
            return 0
    elif len(data) == 1 and id != None:
        select_sql = """SELECT `administrative_name` FROM `administrative_area` WHERE `administrative_id` = %s"""
        try:
            cur.execute(select_sql, (id))
            id_re = cur.fetchone()
        except Exception as erro:
            app.logger.error(erro)
            return 0
        finally:
            closeAll(conn, cur)
        if id_re != '' or id_re != None:
            return id_re[0]
        else:
            return 0
    elif len(data) == 1 and every != None:
        select_sql = """SELECT `administrative_id`,`administrative_name` FROM `administrative_area` """
        try:
            cur.execute(select_sql)
            all_re = cur.fetchall()
        except Exception as erro:
            app.logger.error(erro)
            return 0
        finally:
            closeAll(conn, cur)
        result_list = []
        if all_re != '' or all_re != None:
            for item in all_re:
                result_dict = {}
                result_dict['administrative_id'] = item[0]
                result_dict['administrative_name'] = item[1]
                result_list.append(result_dict)
            return result_list
        else:
            return 0



#地区信息写入数据
def insert_area_info(administrative_id, area_info, governance_situation, year):
    conn = getconn()
    cur = conn.cursor()

    insert_sql = """INSERT INTO `administrative_infos` (`administrative_id`,`area_info`,`governance_situation`,`year`) VALUES (%s,%s,%s,%s)"""
    select_sql = """SELECT `info_id`  FROM `administrative_infos` WHERE `administrative_id` = %s  AND `year`= %s"""
    try:
        insert_re = ''
        select_re = cur.execute(select_sql, (administrative_id, year))
        if select_re != 0:
            return 406
        elif select_re == 0:
            insert_re = cur.execute(insert_sql, (administrative_id, area_info, governance_situation, year))
        if insert_re < 1:
            return 0
        else:
            return 1
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 地区信息删除数据
def delete_area_info(data):
    conn = getconn()
    cur = conn.cursor()
    info_id = data.get('info_id')
    try:
        delete_sql = """DELETE FROM `administrative_infos` WHERE info_id = %s """
        re = cur.execute(delete_sql, (info_id))
        if re < 1:
            return 0
        else:
            return 1
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 地区信息更改数据
def update_info_area(datas):
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
                where_num += 1
                if where_num < len(where_dict):
                    where_sql += "{} = '{}' AND ".format(k, v)
                else:
                    where_sql += "{} = '{}'".format(k, v)
            for k, v in up_dict.items():
                up_num += 1
                if up_num < len(up_dict):
                    up_sql += "{} = '{}', ".format(k, v)
                else:
                    up_sql += "{} = '{}' ".format(k, v)

            update_sql = """UPDATE `administrative_infos` SET """ + up_sql + ' WHERE ' + where_sql
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


#地区信息查询所有数据
def select_area_info():
    conn = getconn()
    cur = conn.cursor()

    try:
        select_sql = """SELECT `info_id`,`administrative_id` ,`area_info` ,`governance_situation` ,`year`  FROM `administrative_infos` """
        re = cur.execute(select_sql)
        if re < 1:
            return 0, 0
        else:
            count = re
            select_admini_name()
            result = cur.fetchall()
            lists = []
            for item in result:
                dict = {}
                for k, v in admini_id_name.items():
                    if item[1] == k:
                        dict['administrative_name'] = admini_id_name[item[1]]
                dict['info_id'] = item[0]
                dict['administrative_id'] = item[1]
                # dict['administrative_name'] = pro_name
                dict['area_info'] = item[2]
                dict['governance_situation'] = item[3]
                dict['year'] = item[4]
                lists.append(dict)
            return lists, count
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 地区信息查询一条数据
def select_area_info_one(data):
    conn = getconn()
    cur = conn.cursor()

    info_id = data['info_id']
    try:
        select_sql = """SELECT `info_id`,`administrative_id` ,`area_info` ,`governance_situation` ,`year`  FROM `administrative_infos` WHERE `info_id` = %s """

        re = cur.execute(select_sql, (info_id))
        if re < 1:
            return 0
        else:
            select_admini_name()
            item = cur.fetchone()
            # pro_name = select_pro_by_id(item[1])
            dict = {}
            for k, v in admini_id_name.items():
                if item[1] == k:
                    dict['administrative_name'] = admini_id_name[item[1]]
            dict['info_id'] = item[0]
            dict['administrative_id'] = item[1]
            # dict['administrative_name'] = pro_name
            dict['area_info'] = item[2]
            dict['governance_situation'] = item[3]
            dict['year'] = item[4]
            return dict
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 分页查询地区信息数据
def select_area_info_page(page, count):
    conn = getconn()
    cur = conn.cursor()
    try:
        select_info = '''SELECT `info_id`,`administrative_id`,`area_info`,`governance_situation`,`year` FROM `administrative_infos` LIMIT %s, %s;'''
        count = count
        if int(page) == 1 or int(page) == 0:
            page_t = 0
        else:
            page_t = (int(page) - 1) * int(count)
        re = cur.execute(select_info, (int(page_t), int(count)))
        if re < 1:
            return 0
        else:
            select_admini_name()
            result = cur.fetchall()
            lists = []
            for item in result:
                dict = {}
                for k, v in admini_id_name.items():
                    if item[1] == k:
                        dict['administrative_name'] = admini_id_name[item[1]]
                # pro_name = select_pro_by_id(item[1])
                dict['info_id'] = item[0]
                dict['administrative_id'] = item[1]
                dict['area_info'] = item[2]
                dict['governance_situation'] = item[3]
                dict['year'] = item[4]

                lists.append(dict)
            return lists
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 历届选举信息写入数据
def insert_election_info(administrative_id, elector, election_score, election_parties, period, year):
    conn = getconn()
    cur = conn.cursor()

    insert_sql = """INSERT INTO `previous_elections` (`administrative_id`,`elector`,`election_score`,`election_parties`,`period`,`year`) VALUES (%s,%s,%s,%s,%s,%s)"""
    select_sql = """SELECT `id`  FROM `previous_elections` WHERE `administrative_id` = %s AND `elector`= %s AND `election_score`= %s AND `election_parties`= %s AND `period`= %s AND `year`= %s"""
    try:
        insert_re = ''
        select_re = cur.execute(select_sql,
                                (administrative_id, elector, election_score, election_parties, period, year))
        if select_re != 0:
            return 406
        elif select_re == 0:
            insert_re = cur.execute(insert_sql,
                                    (administrative_id, elector, election_score, election_parties, period, year))
        if insert_re < 1:
            return 0
        else:
            return 1
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 历届选举信息删除数据
def delete_election_info(data):
    conn = getconn()
    cur = conn.cursor()
    id = data.get('id')
    try:
        delete_sql = """DELETE FROM `previous_elections` WHERE id = %s """
        re = cur.execute(delete_sql, (id))
        if re < 1:
            return 0
        else:
            return 1
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 更改历届选举信息数据
def update_election_info(datas):
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
                where_num += 1
                if where_num < len(where_dict):
                    where_sql += "{} = '{}' AND ".format(k, v)
                else:
                    where_sql += "{} = '{}'".format(k, v)
            for k, v in up_dict.items():
                up_num += 1
                if up_num < len(up_dict):
                    up_sql += "{} = '{}', ".format(k, v)
                else:
                    up_sql += "{} = '{}' ".format(k, v)
            update_sql = """UPDATE `previous_elections` SET """ + up_sql + ' WHERE ' + where_sql
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


# 查询历届选举信息数据所有数据
def select_election_all():
    conn = getconn()
    cur = conn.cursor()

    try:
        select_sql = """SELECT `id`,`administrative_id` ,`elector` ,`election_score` ,`election_parties` ,`period` ,`year` FROM `previous_elections` """
        re = cur.execute(select_sql)
        if re < 1:
            return 0, 0
        else:
            count = re
            # select_admini_name()
            result = cur.fetchall()
            lists = []
            for item in result:
                dict = {}
                for k, v in admini_id_name.items():
                    if item[1] == k:
                        dict['administrative_name'] = admini_id_name[item[1]]
                dict['id'] = item[0]
                dict['administrative_id'] = item[1]
                dict['elector'] = item[2]
                dict['election_score'] = item[3]
                dict['election_parties'] = item[4]
                dict['period'] = item[5]
                dict['year'] = item[6]

                lists.append(dict)
            return lists, count
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn,cur)


# 历届选举信息根据id查询单条数据
def select_election_info_one(data):
    conn = getconn()
    cur = conn.cursor()

    id = data['id']
    try:
        select_sql = """SELECT `id`,`administrative_id` ,`elector` ,`election_score` ,`election_parties` ,`period` ,`year` FROM `previous_elections` WHERE `id` = %s """
        re = cur.execute(select_sql, (id))
        if re < 1:
            return 0
        else:
            select_admini_name()
            item = cur.fetchone()
            dict = {}
            for k, v in admini_id_name.items():
                if item[1] == k:
                    dict['administrative_name'] = admini_id_name[item[1]]
            dict['id'] = item[0]
            dict['administrative_id'] = item[1]
            # dict['administrative_name'] = pro_name
            dict['elector'] = item[2]
            dict['election_score'] = item[3]
            dict['election_parties'] = item[4]
            dict['period'] = item[5]
            dict['year'] = item[6]

            return dict
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 分页查询历届选举信息情况数据
def select_election_info_page(page, count):
    conn = getconn()
    cur = conn.cursor()
    try:
        select_info = '''SELECT `id`,`administrative_id`,`elector`,`election_score`,`election_parties`,`period`,`year` FROM `previous_elections` LIMIT %s, %s;'''
        # select_sql2 = """SELECT `*` FROM `previous_elections` """
        # re2 = cur.execute(select_sql2)
        # all_pages = re2 / int(count)
        # if all_pages < 1:
        #     all_pages = 1
        # else:
        #     all_pages = math.ceil(all_pages)
        count = count
        if int(page) == 1 or int(page) == 0:
            page_t = 0
        else:
            page_t = (int(page) - 1) * int(count)
        re = cur.execute(select_info, (int(page_t), int(count)))
        if re < 1:
            return 0
        else:
            select_admini_name()
            result = cur.fetchall()
            lists = []
            for item in result:
                # pro_name = select_pro_by_id(item[1])
                dict = {}
                for k, v in admini_id_name.items():
                    if item[1] == k:
                        dict['administrative_name'] = admini_id_name[item[1]]
                dict['id'] = item[0]
                dict['administrative_id'] = item[1]
                # dict['administrative_name'] = pro_name
                dict['elector'] = item[2]
                dict['election_score'] = item[3]
                dict['election_parties'] = item[4]
                dict['period'] = item[5]
                dict['year'] = item[6]
                # dict['all_pages'] = all_pages
                lists.append(dict)
            return lists
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


admini_id_name = {}


def select_admini_name():
    conn = getconn()
    cur = conn.cursor()

    try:
        select_sql = """SELECT `administrative_id`, `administrative_name` FROM `administrative_area` """
        re = cur.execute(select_sql)
        if re:
            items = cur.fetchall()
            for item in items:
                admini_id_name[item[0]] = item[1]
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)

#根据地区编号查询地区信息数据
def select_area_code_info(administrative_id, page, count_info):
    conn = getconn()
    cur = conn.cursor()
    administrative_id = administrative_id
    try:
        select_info = '''SELECT `info_id`,`administrative_id` ,`area_info` ,`governance_situation` ,`year` FROM `administrative_infos` WHERE `administrative_id` = %s LIMIT %s, %s;'''
        select_count = '''SELECT `info_id`,`administrative_id` ,`area_info` ,`governance_situation` ,`year` FROM `administrative_infos` WHERE `administrative_id` = %s '''

        count_info = count_info
        if int(page) == 1 or int(page) == 0:
            page_t = 0
        else:
            page_t = (int(page) - 1) * int(count_info)
        re2 = cur.execute(select_count, (administrative_id))
        re = cur.execute(select_info, (administrative_id, int(page_t), int(count_info)))
        if re < 1:
            return 0, 0
        else:
            count = re2
            select_admini_name()
            result = cur.fetchall()
            lists = []
            for item in result:
                dict = {}
                for k, v in admini_id_name.items():
                    if item[1] == k:
                        dict['administrative_name'] = admini_id_name[item[1]]
                # pro_name = select_pro_by_id(item[1])
                dict['info_id'] = item[0]
                dict['administrative_id'] = item[1]
                dict['area_info'] = item[2]
                dict['governance_situation'] = item[3]
                dict['year'] = item[4]

                lists.append(dict)
            return lists, count
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)



#历届选举信息根据地区编号查询数据
def select_election_code_info(administrative_id, page, count_info):
    conn = getconn()
    cur = conn.cursor()
    administrative_id = administrative_id

    try:
        select_info = '''SELECT `id`,`administrative_id`,`elector`,`election_score`,`election_parties`,`period`,`year` FROM `previous_elections` WHERE `administrative_id` = %s LIMIT %s, %s;'''
        select_count = '''SELECT `id`,`administrative_id`,`elector`,`election_score`,`election_parties`,`period`,`year` FROM `previous_elections` WHERE `administrative_id` = %s '''

        count_info = count_info
        if int(page) == 1 or int(page) == 0:
            page_t = 0
        else:
            page_t = (int(page) - 1) * int(count_info)
        re2 = cur.execute(select_count, (administrative_id))
        re = cur.execute(select_info, (administrative_id, int(page_t), int(count_info)))
        if re < 1:
            return 0, 0
        else:
            count = re2
            select_admini_name()
            result = cur.fetchall()
            lists = []
            for item in result:
                dict = {}
                for k, v in admini_id_name.items():
                    if item[1] == k:
                        dict['administrative_name'] = admini_id_name[item[1]]
                dict['id'] = item[0]
                dict['administrative_id'] = item[1]
                # dict['administrative_name'] = pro_name
                dict['elector'] = item[2]
                dict['election_score'] = item[3]
                dict['election_parties'] = item[4]
                dict['period'] = item[5]
                dict['year'] = item[6]
                lists.append(dict)
            return lists, count
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)
