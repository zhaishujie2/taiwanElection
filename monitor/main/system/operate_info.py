# coding=utf-8
from monitor.util.mysql_util import getconn,closeAll
from monitor import app

#写入数据
def insert_info(datas):
    conn = getconn()
    cur = conn.cursor()

    administrative_id = datas.get('id')
    administrative_name = datas.get('name')
    year = datas.get('year')
    facebook_url = datas.get('url')
    try:
        insert_sql = """INSERT INTO `spider_infos` (`administrative_id`,`administrative_name`,`year`,`facebook_url`) VALUES (%s,%s,%s,%s)"""
        # print(insert_sql)
        re = cur.execute(insert_sql,(administrative_id,administrative_name,year,facebook_url))
        # print(re)
        if re < 1:
            return "0"
        else:
            return "1"
    except Exception as erro:
        app.logger.error(erro)
        return str(erro)
    finally:
        closeAll(conn,cur)

#删除数据
def delete_info(data):
    conn = getconn()
    cur = conn.cursor()
    ids = data.get('id')
    try:
        delete_sql = """DELETE FROM `spider_infos` WHERE id = %s """
        re = cur.execute(delete_sql,(ids))
        if re < 1:
            return "0"
        else:
            return "1"
    except Exception as erro:
        app.logger.error(erro)
        return str(erro)
    finally:
        closeAll(conn,cur)

#修改数据
def update_info(datas):
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
            for k,v in where_dict.items():
                where_num += 1
                if where_num < len(where_dict):
                    where_sql += "{} = '{}' AND ".format(k,v)
                else:
                    where_sql += "{} = '{}'".format(k,v)
            for k,v in up_dict.items():
                up_num += 1
                if up_num < len(up_dict):
                    up_sql += "{} = '{}', ".format(k,v)
                else:
                    up_sql += "{} = '{}' ".format(k,v)

            update_sql = """UPDATE `spider_infos` SET """ + up_sql +' WHERE '+ where_sql
            # print(update_sql)
            re = cur.execute(update_sql)
            if re < 1 :
                return '0'
            else:
                return '1'
        except Exception as erro:
            app.logger.error(erro)
            return str(erro)
        finally:
            closeAll(conn,cur)

#查询数据
def select_info(datas):
    conn = getconn()
    cur = conn.cursor()

    try:
        where_sql = ''
        num = 0
        for k,v in datas.items():
            num += 1
            if num < len(datas):
                where_sql += "{} = '{}'".format(k,v) + ' AND '
            else:
                where_sql += "{} = '{}'".format(k,v)

        select_sql = """SELECT * FROM `spider_infos` WHERE  """ + where_sql
        re = cur.execute(select_sql)
        if re < 1:
            return '0'
        else:
            result = cur.fetchall()
            lists = []
            for item in result:
                dict = {}
                dict['administrative_id'] = item[1]
                dict['administrative_name'] = item[2]
                dict['year'] = item[3]
                dict['url'] = item[4]
                lists.append(dict)
            return lists,'1'
    except Exception as erro:
        app.logger.error(erro)
        return str(erro),'2'
    finally:
        closeAll(conn,cur)

#查询候选人是否存在
def get_is_candidate(data):
    administrative_id = data.get('administrative_id')
    username = data.get('username')
    year = data.get('year')
    conn = getconn()
    cur = conn.cursor()
    select_sql = """SELECT `username` FROM `candidate` WHERE `administrative_id` = %s AND `username` = %s AND `year` = %s"""
    region_number_select_sql = """SELECT `administrative_id` FROM `administrative_area`"""
    try:
        count = cur.execute(select_sql,(administrative_id,username,year))
        cur.execute(region_number_select_sql)
        region_number_re = cur.fetchall()
        region_number_list = []
        for item in region_number_re:
            region_number_list.append(item)
        if administrative_id not in region_number_list:
            app.logger.error("输入正确的地区代码")
            return 406
    except Exception as erro:
        app.logger.errr(erro)
        return str(erro)
    finally:
        closeAll(conn,cur)
    return count

#根据id查询单条数据
def get_one_infos(info_type,data):
    types = info_type
    ids = data.get('id')
    conn = getconn()
    cur = conn.cursor()
    if types == '1':#查询Facebook
        facebook_select_sql = """SELECT `id`,`administrative_id`,`administrative_name`,`year`,`facebook_url` FROM `spider_infos` WHERE `id` = %s"""
        try:
            cur.execute(facebook_select_sql,(ids))
            facebook_re = cur.fetchall()
        except Exception as erro:
            app.logger.error(erro)
            return 0
        finally:
            closeAll(conn,cur)
        facebook_dict = {}
        facebook_list = []
        for item in facebook_re:
            facebook_dict['id'] = item[0]
            facebook_dict['administrative_id'] = item[1]
            facebook_dict['administrative_name'] = item[2]
            facebook_dict['year'] = item[3]
            facebook_dict['facebook_url'] = item[4]
        facebook_list.append(facebook_dict)
        return facebook_list
    elif types == '2':#查询地区信息
        administrative_select_sql = """SELECT `info_id`,`administrative_id`,`area_info`,`governance_situation`,`year` FROM `administrative_infos` WHERE `info_id` = %s"""
        try:
            cur.execute(administrative_select_sql,(ids))
            administrative_re = cur.fetchall()
        except Exception as erro:
            app.logger.error(erro)
            return 0
        finally:
            closeAll(conn,cur)
        administrative_dict = {}
        administrative_list = []
        for item in administrative_re:
            administrative_dict['id'] = item[0]
            administrative_dict['administrative_id'] = item[1]
            administrative_dict['area_info'] = item[2]
            administrative_dict['governance_situation'] = item[3]
            administrative_dict['year'] = item[4]
        administrative_list.append(administrative_dict)
        return administrative_list
    elif types == '3':#查询后寻人信息
        candidate_select_sql ="""SELECT `job`,`department`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`stain`,`sex`,`name_en`,`birthday`,`birthplace`,`taiwan_id`,`passport`,`personal_webpage`,`personal_phone`,`work_phone`,`email`,`address`,`education`,`partisan`,`name`,`candidate_id` FROM `candidate_personnel_information` WHERE  `candidate_id` = %s"""
        try:
            cur.execute(candidate_select_sql,(ids))
            candidate_re = cur.fetchall()
        except Exception as erro:
            app.logger.error(erro)
            return 0
        finally:
            closeAll(conn,cur)
        candidate_list = []
        information = {}
        candidate_dict = {}
        for item in candidate_re:
            candidate_dict['candidate_id'] = item[23]
            candidate_dict['name'] = item[22]
            candidate_dict['job'] = item[0]
            candidate_dict['department'] = item[1]
            candidate_dict['family'] = item[2]
            candidate_dict['job_manager'] = item[3]
            candidate_dict['political'] = item[4]
            candidate_dict['society'] = item[5]
            candidate_dict['competition'] = item[6]
            candidate_dict['situation'] = item[7]
            candidate_dict['stain'] = item[8]
            information['sex'] = item[9]
            information['name_en'] = item[10]
            information['birthday'] = str(item[11])
            information['birthplace'] = item[12]
            information['taiwan_id'] = item[13]
            information['passport'] = item[14]
            information['personal_webpage'] = item[15]
            information['personal_phone'] = item[16]
            information['work_phone'] = item[17]
            information['email'] = item[18]
            information['address'] = item[19]
            information['education'] = item[20]
            information['partisan'] = item[21]
            candidate_dict['information'] = information
        candidate_list.append(candidate_dict)
        return candidate_list
    elif types == '4':#查询团队成员信息
        member_select_sql ="""SELECT `job`,`department`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`stain`,`sex`,`name_en`,`birthday`,`birthplace`,`taiwan_id`,`passport`,`personal_webpage`,`personal_phone`,`work_phone`,`email`,`address`,`education`,`partisan`,`name`,`id` FROM `personnel_information` WHERE `id` = %s"""
        try:
            cur.execute(member_select_sql,(ids))
            member_re = cur.fetchall()
        except Exception as erro:
            app.logger.error(erro)
            return 0
        finally:
            closeAll(conn,cur)
        member_dict = {}
        information = {}
        member_list = []
        for item in member_re:
            member_dict['id'] = item[23]
            member_dict['name'] = item[22]
            member_dict['job'] = item[0]
            member_dict['department'] = item[1]
            member_dict['family'] = item[2]
            member_dict['job_manager'] = item[3]
            member_dict['political'] = item[4]
            member_dict['society'] = item[5]
            member_dict['competition'] = item[6]
            member_dict['situation'] = item[7]
            member_dict['stain'] = item[8]
            information['sex'] = item[9]
            information['name_en'] = item[10]
            information['birthday'] = str(item[11])
            information['birthplace'] = item[12]
            information['taiwan_id'] = item[13]
            information['passport'] = item[14]
            information['personal_webpage'] = item[15]
            information['personal_phone'] = item[16]
            information['work_phone'] = item[17]
            information['email'] = item[18]
            information['address'] = item[19]
            information['education'] = item[20]
            information['partisan'] = item[21]
            member_dict['information'] = information
        member_list.append(member_dict)
        return member_list


#地区代码
def get_region_dict(data):
    name = data.get('name')
    id  = data.get('id')
    every = data.get('every')
    conn= getconn()
    cur = conn.cursor()
    if len(data) == 1 and name != None:
        select_sql = """SELECT `administrative_id` FROM `administrative_area` WHERE `administrative_name` = %s"""
        try:
            cur.execute(select_sql,(name))
            name_re = cur.fetchone()
        except Exception as erro:
            app.logger.error(erro)
            return 0
        finally:
            closeAll(conn,cur)
        if name_re != '' or name_re != None:
            return name_re[0]
        else:
            return 0
    elif len(data) == 1 and id != None:
        select_sql = """SELECT `administrative_name` FROM `administrative_area` WHERE `administrative_id` = %s"""
        try:
            cur.execute(select_sql,(id))
            id_re = cur.fetchone()
        except Exception as erro:
            app.logger.error(erro)
            return 0
        finally:
            closeAll(conn,cur)
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
            closeAll(conn,cur)
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



# if __name__ == '__main__':
#     # a = insert_info('7017','李晨','2018','www.facebook.com')
#     a = delete_info(11)#{"administrative_id":"7019","administrative_name":"李晨"}
#     # a = select_info({"administrative_id":"7017","administrative_name":"李晨","year":"2018","facebook_url":"www.baidu.com"})
#     # a = update_info(up_dict={"administrative_id":"7020","administrative_name":"lichen"},where_dict={"administrative_id":"7019","administrative_name":"李晨"})
#     # a = select_info({"administrative_name":"李晨","year":"2020"})
#     print(a)


