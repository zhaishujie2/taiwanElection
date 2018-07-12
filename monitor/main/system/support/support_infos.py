# coding=utf-8
from monitor.main.system.util import get_date_item
from monitor.util.mysql_util import getconn, closeAll
from monitor import app

#添加民调数据
def insert_support(datas):
    conn = getconn()
    cur = conn.cursor()
    times = datas.get('support_time')
    support_time = get_date_item(times)
    candidate_id = datas.get('candidate_id')
    if candidate_id == None or support_time == None:
        app.logger.error('侯选人id或者民调月份未写入')
        return 0
    twenty = datas.get('20s-30s')
    if twenty == None:
        twenty = '0.00'
    thirty = datas.get('30s-40s')
    if thirty == None:
        thirty = '0.00'
    forty = datas.get('40s-50s')
    if forty == None:
        forty = '0.00'
    fifty = datas.get('50s-60s')
    if fifty == None:
        fifty = '0.00'
    sixty = datas.get('60s-70s')
    if sixty == None:
        sixty = '0.00'
    seventy = datas.get('70s')
    if seventy == None:
        seventy = '0.00'
    network_support = datas.get('network_support')
    if network_support == None:
        network_support = '0.00'
    total_support = datas.get('total_support')
    if total_support == None:
        total_support = '0.00'
    insert_support_sql = """INSERT INTO `poll_support` (`candidate_id`,`20s-30s`,`30s-40s`,`40s-50s`,`50s-60s`,`60s-70s`,`70s`,`network_support`,`total_support`,`support_time`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    select_support_sql = """SELECT `support_time`  FROM `poll_support` WHERE `support_time` = %s AND `candidate_id`= %s """
    try:
        insert_re = ''
        select_re = cur.execute(select_support_sql,(support_time,candidate_id))
        if select_re != 0:
            app.logger.error('该月份数据已经存在')
            return 406
        elif select_re == 0:
            insert_re = cur.execute(insert_support_sql,(candidate_id,twenty,thirty,forty,fifty,sixty,seventy,network_support,total_support,support_time))
        if insert_re < 1:
            app.logger.error('民调数据未写入')
            return 0
        else:
            app.logger.error('民调数据写入成功')
            return 1
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


#获取民调数据
def select_support(datas):
    conn = getconn()
    cur = conn.cursor()
    candidate_id =  datas.get('candidate_id')
    ids=  datas.get('id')

    try:
        suopport_all_select_sql = """SELECT `id`,`candidate_id`,`20s-30s`,`30s-40s`,`40s-50s`,`50s-60s`,`60s-70s`,`70s`,`network_support`,`total_support`,`support_time` FROM `poll_support` WHERE  `candidate_id` = %s LIMIT %s,%s"""
        suopport_one_select_sql = """SELECT `id`,`candidate_id`,`20s-30s`,`30s-40s`,`40s-50s`,`50s-60s`,`60s-70s`,`70s`,`network_support`,`total_support`,`support_time` FROM `poll_support` WHERE  `id` = %s"""
        if candidate_id != None:
            page_number = datas.get('page_number')
            page_size = datas.get('page_size')
            start = (int(page_number) - 1) * int(page_size)
            re = cur.execute(suopport_all_select_sql,(candidate_id,start,int( page_size)))
            if re < 1:
                app.logger.error('无某一候选人民调所有信息')
                return 0
        else:
            re = cur.execute(suopport_one_select_sql,(ids))
            if re < 1:
                app.logger.error('无某一民调信息')
                return 0
        result = cur.fetchall()
        lists = []
        for item in result:
            dict = {}
            dict['id'] = item[0]
            dict['candidate_id'] = item[1]
            dict['20s-30s'] = item[2]
            dict['30s-40s'] = item[3]
            dict['40s-50s'] = item[4]
            dict['50s-60s'] = item[5]
            dict['60s-70s'] = item[6]
            dict['70s'] = item[7]
            dict['network_support'] = item[8]
            dict['total_support'] = item[9]
            dict['support_time'] = item[10]
            lists.append(dict)
        return lists
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 删除民调数据
def delete_support(data):
    conn = getconn()
    cur = conn.cursor()
    ids = data.get('id')
    try:
        delete_support_sql = """DELETE FROM `poll_support` WHERE id = %s """
        re = cur.execute(delete_support_sql, (ids))
        if re < 1:
            conn.rollback()
            cur.close()
            conn.close()
            return 0
        else:
            return 1
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 修改民调数据
def update_support(datas):
    where_dict = datas.get('where_dict')
    up_dict = datas.get('up_dict')
    if len(where_dict) == 0 or len(up_dict) == 0:
        if len(where_dict) == 0:
            app.logger.error( "更新条件不能为空")
            return 0
        if len(up_dict) == 0:
            app.logger.error( "更新内容不能为空")
            return 0
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
                    up_sql += "`{}` = '{}', ".format(k, v)
                else:
                    up_sql += "`{}` = '{}' ".format(k, v)
            update_support_sql = """UPDATE `poll_support` SET """ + up_sql + ' WHERE ' + where_sql
            support_re = cur.execute(update_support_sql)
            if support_re < 1:
                app.logger.error('民调信息未更新成功')
                conn.rollback()
                cur.close()
                conn.close()
                return 0
            else:
                closeAll(conn,cur)
                app.logger.error('民调信息更新成功')
                return 1
        except Exception as erro:
            app.logger.error(erro)
            return 0


#添加党派数据
def insert_partisan(datas):
    conn = getconn()
    cur = conn.cursor()
    partisan = datas.get('partisan')

    insert_support_sql = """INSERT INTO `partisan` (`partisan`) VALUES (%s)"""
    select_support_sql = """SELECT `partisan`  FROM `partisan` WHERE `partisan` = %s """
    try:
        insert_re = ''
        select_re = cur.execute(select_support_sql,(partisan))
        if select_re != 0:
            app.logger.error('党派数据已经存在')
            return 406
        elif select_re == 0:
            insert_re = cur.execute(insert_support_sql,(partisan))
        if insert_re < 1:
            app.logger.error('党派数据未写入')
            return 0
        else:
            app.logger.error('党派数据写入成功')
            return 1
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


#获取党派数据
def select_partisan(datas):
    conn = getconn()
    cur = conn.cursor()
    ids=  datas.get('id')
    try:
        partisan_all_select_sql = """SELECT `id`,`partisan`,`partisan_image` FROM `partisan` LIMIT %s,%s"""
        partisan_one_select_sql = """SELECT `id`,`partisan`,`partisan_image` FROM `partisan` WHERE  `id` = %s"""
        if ids == None:
            page_number = datas.get('page_number')
            page_size = datas.get('page_size')
            start = (int(page_number) - 1) * int(page_size)
            re = cur.execute(partisan_all_select_sql,(start,int( page_size)))
            if re < 1:
                app.logger.error('党派所有信息')
                return 0
        else:
            re = cur.execute(partisan_one_select_sql,(ids))
            if re < 1:
                app.logger.error('无某一党派信息')
                return 0
        result = cur.fetchall()
        lists = []
        for item in result:
            dict = {}
            dict['id'] = item[0]
            dict['partisan'] = item[1]
            dict['partisan_image'] = item[2]
            lists.append(dict)
        return lists
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 删除党派数据
def delete_partisan(data):
    conn = getconn()
    cur = conn.cursor()
    ids = data.get('id')
    try:
        delete_support_sql = """DELETE FROM `partisan` WHERE id = %s """
        re = cur.execute(delete_support_sql, (ids))
        if re < 1:
            conn.rollback()
            cur.close()
            conn.close()
            app.logger.error('该党派信息未删除')
            return 0
        else:
            app.logger.error('该党派信息已删除')
            return 1
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)

# 根据地区返回该地区的所有年份
def get_all_years(info_type, data):
    conn = getconn()
    cur = conn.cursor()

    if info_type == 'years':
        try:
            administrative_id = data.get('administrative_id')
            years_select_sql = """SELECT `year` FROM `candidate` WHERE `administrative_id` = %s GROUP BY `year`"""
            re = cur.execute(years_select_sql, (administrative_id))
            if re < 1:
                return []
            else:
                result = cur.fetchall()
                result_lists = []
                mid_list = []
                dict = {}
                for item in result:
                    mid_list.append(item[0])
                dict['years'] = mid_list
                result_lists.append(dict)
                return result_lists
        except Exception as erro:
            app.logger.error(erro)
            return 0
        finally:
            closeAll(conn, cur)
    elif info_type == 'candidates':
        try:
            year = data.get('year')
            administrative_id = data.get('administrative_id')
            candidates_select_sql = """SELECT `candidate_id`,`username` FROM `candidate` WHERE `year` = %s AND `administrative_id` = %s"""
            re = cur.execute(candidates_select_sql, (year, administrative_id))
            if re < 1:
                return 0
            else:
                result = cur.fetchall()
                lists = []
                for item in result:
                    dict = {}
                    dict['candidate_id'] = item[0]
                    dict['name'] = item[1]
                    lists.append(dict)
                return lists
        except Exception as erro:
            app.logger.error(erro)
            return 0
        finally:
            closeAll(conn, cur)



# 修改党派数据
def update_partisan(datas):
    where_dict = datas.get('where_dict')
    up_dict = datas.get('up_dict')
    if len(where_dict) == 0 or len(up_dict) == 0:
        if len(where_dict) == 0:
            app.logger.error( "更新条件不能为空")
            return 0
        if len(up_dict) == 0:
            app.logger.error( "更新内容不能为空")
            return 0
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
                    up_sql += "`{}` = '{}', ".format(k, v)
                else:
                    up_sql += "`{}` = '{}' ".format(k, v)
            update_support_sql = """UPDATE `partisan` SET """ + up_sql + ' WHERE ' + where_sql
            support_re = cur.execute(update_support_sql)
            if support_re < 1:
                app.logger.error('民调信息未更新成功')
                conn.rollback()
                cur.close()
                conn.close()
                return 0
            else:
                closeAll(conn,cur)
                app.logger.error('民调信息更新成功')
                return 1
        except Exception as erro:
            app.logger.error(erro)
            return 0


# 做分页
def get_pages(datas):
    conn = getconn()
    cur = conn.cursor()
    info_type = datas.get('info_type')
    try:
        if info_type == '6':#民调数据所有数据
            candidate_id =  datas.get('candidate_id')
            suopport_all_select_sql = """SELECT `id` FROM `poll_support` WHERE  `candidate_id` = %s"""
            suopport_all_count = cur.execute(suopport_all_select_sql,(candidate_id))
            if suopport_all_count < 1:
                app.logger.error('无某一侯选人所有民调信息')
                return 0
            else:
                return suopport_all_count
        elif info_type == '7':#党派数据所有数据
            partisan_all_select_sql = """SELECT `id` FROM `partisan`"""
            partisan_all_count = cur.execute(partisan_all_select_sql)
            if partisan_all_count < 1:
                app.logger.error('无所有党派信息')
                return 0
            else:
                return partisan_all_count
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)

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
