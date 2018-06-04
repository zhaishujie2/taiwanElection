# coding=utf-8
from monitor.util.mysql_util import getconn, closeAll
from monitor import app
import os,sys

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


# facebook写入数据
def insert_info(auto_id, datas):
    conn = getconn()
    cur = conn.cursor()

    administrative_id = datas.get('administrative_id')
    if datas.get('administrative_name') != None:
        administrative_name = datas.get('administrative_name')
    else:
        administrative_name = datas.get('username')
    year = datas.get('year')
    facebook_url = datas.get('facebook_url')
    insert_sql = """INSERT INTO `spider_infos` (`id`,`administrative_id`,`administrative_name`,`year`,`facebook_url`) VALUES (%s,%s,%s,%s,%s)"""
    select_sql = """SELECT `id`  FROM `spider_infos` WHERE `administrative_id` = %s AND `administrative_name`= %s AND `year`= %s AND `facebook_url`= %s"""
    try:
        insert_re = ''
        select_re = cur.execute(select_sql, (administrative_id, administrative_name, year, facebook_url))
        if select_re != 0:
            return 406
        elif select_re == 0:
            insert_re = cur.execute(insert_sql, (auto_id, administrative_id, administrative_name, year, facebook_url))
        if insert_re < 1:
            return 0
        else:
            return 1
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# facebook删除数据
def delete_info(data):
    conn = getconn()
    cur = conn.cursor()
    ids = data.get('candidate_id')
    try:
        delete_sql = """DELETE FROM `spider_infos` WHERE id = %s """
        re = cur.execute(delete_sql, (ids))
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


# facebook修改数据
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

            update_sql = """UPDATE `spider_infos` SET """ + up_sql + ' WHERE ' + where_sql
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


# facebook查询数据
def select_info(datas):
    conn = getconn()
    cur = conn.cursor()
    try:
        where_sql = ''
        if len(datas) == 0:
            where_sql = '1 = 1 '
        else:
            for k, v in datas.items():
                where_sql += "{} = '{}'".format(k, v)
        select_sql = """SELECT `administrative_id`,`administrative_name`,`year`,`facebook_url`,`id` FROM `spider_infos` WHERE  """ + where_sql
        re = cur.execute(select_sql)
        if re < 1:
            return 0
        else:
            result = cur.fetchall()
            lists = []
            for item in result:
                dict = {}
                dict['administrative_id'] = item[0]
                dict['administrative_name'] = item[1]
                dict['year'] = item[2]
                dict['url'] = item[3]
                dict['id'] = item[4]
                lists.append(dict)
            return lists
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 查询候选人是否存在
def get_is_candidate(data):
    administrative_id = data.get('administrative_id')
    username = data.get('username')
    year = data.get('year')
    conn = getconn()
    cur = conn.cursor()
    select_sql = """SELECT `username` FROM `candidate` WHERE `administrative_id` = %s AND `username` = %s AND `year` = %s"""
    region_number_select_sql = """SELECT `administrative_id` FROM `administrative_area`"""
    count = ''
    try:
        count = cur.execute(select_sql, (administrative_id, username, year))
        cur.execute(region_number_select_sql)
        region_number_re = cur.fetchall()
        region_number_list = []
        for item in region_number_re:
            region_number_list.append(str(item[0]))
        if administrative_id not in region_number_list:
            app.logger.error("输入正确的地区代码")
            return 407
    except Exception as erro:
        app.logger.errr(erro)
        return 0
    finally:
        closeAll(conn, cur)
        return count


# 根据id查询单条数据
def get_one_infos(info_type, data):
    types = info_type
    ids = data.get('id')
    conn = getconn()
    cur = conn.cursor()
    if types == '1':  # 查询Facebook
        # facebook_select_sql = """SELECT `id`,`administrative_id`,`administrative_name`,`year`,`facebook_url` FROM `spider_infos` WHERE `id` = %s"""
        facebook_select_sql = """SELECT `id`,`administrative_id`,`administrative_name`,`year`,`facebook_url`,`image_name` FROM(SELECT * FROM `spider_infos` )a ,(SELECT `candidate_id` as ids,`image_name`  FROM `candidate_personnel_information` )b WHERE a.id = b.ids  AND `id` = %s"""
        try:
            cur.execute(facebook_select_sql, (ids))
            facebook_re = cur.fetchall()
        except Exception as erro:
            app.logger.error(erro)
            return 0
        finally:
            closeAll(conn, cur)
        facebook_dict = {}
        facebook_list = []
        for item in facebook_re:
            facebook_dict['id'] = item[0]
            facebook_dict['administrative_id'] = item[1]
            facebook_dict['administrative_name'] = item[2]
            facebook_dict['year'] = item[3]
            facebook_dict['facebook_url'] = item[4]
            facebook_dict['image_name'] = item[5]
        facebook_list.append(facebook_dict)
        return facebook_list
    elif types == '2':  # 查询地区信息
        administrative_select_sql = """SELECT `info_id`,`administrative_id`,`area_info`,`governance_situation`,`year` FROM `administrative_infos` WHERE `info_id` = %s"""
        try:
            cur.execute(administrative_select_sql, (ids))
            administrative_re = cur.fetchall()
        except Exception as erro:
            app.logger.error(erro)
            return 0
        finally:
            closeAll(conn, cur)
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
    elif types == '3':  # 查询候选人信息
        candidate_select_sql = """SELECT `job`,`department`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`stain`,`sex`,`name_en`,`birthday`,`birthplace`,`taiwan_id`,`passport`,`personal_webpage`,`personal_phone`,`work_phone`,`email`,`address`,`education`,`partisan`,`name`,`candidate_id`,`image_name` FROM `candidate_personnel_information` WHERE  `candidate_id` = %s"""
        try:
            cur.execute(candidate_select_sql, (ids))
            candidate_re = cur.fetchall()
        except Exception as erro:
            app.logger.error(erro)
            return 0
        finally:
            closeAll(conn, cur)
        candidate_list = []
        information = {}
        candidate_dict = {}
        for item in candidate_re:
            candidate_dict['image_name'] = item[24]
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
    elif types == '4':  # 查询团队成员信息
        member_select_sql = """SELECT `job`,`department`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`stain`,`sex`,`name_en`,`birthday`,`birthplace`,`taiwan_id`,`passport`,`personal_webpage`,`personal_phone`,`work_phone`,`email`,`address`,`education`,`partisan`,`name`,`id`,`image_name` FROM `personnel_information` WHERE `id` = %s"""
        try:
            cur.execute(member_select_sql, (ids))
            member_re = cur.fetchall()
        except Exception as erro:
            app.logger.error(erro)
            return 0
        finally:
            closeAll(conn, cur)
        member_dict = {}
        information = {}
        member_list = []
        for item in member_re:
            member_dict['image_name'] = item[24]
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


# 删除候选人信息或者团队人员信息
def delete_people_information(type, content):
    conn = getconn()
    cur = conn.cursor()
    candidate_id = ''

    if content.get('candidate_id') != '' and content.get('candidate_id') != None:
        candidate_id = content.get('candidate_id')
    else:
        candidate_id = content.get('id')
    info_type = content.get('type')
    try:
        if info_type == '1':
            # spider_re = delete_info(content)
            delete_sql = """DELETE FROM `spider_infos` WHERE id = %s """
            spider_re = cur.execute(delete_sql,(candidate_id))
            if spider_re < 1:
                conn.rollback()
                cur.close()
                conn.close()
                return 0
            elif spider_re == 1:
                delete_candidate_personnel_information_sql = """DELETE FROM `candidate_personnel_information` WHERE `candidate_id` = %s """
                delete_candidate_sql = """DELETE FROM `candidate` WHERE `candidate_id` = %s """
                information_re = cur.execute(delete_candidate_personnel_information_sql, (candidate_id))
                if information_re < 1:
                    conn.rollback()
                    cur.close()
                    conn.close()
                    return 0
                else:
                    candidate_re = cur.execute(delete_candidate_sql, (candidate_id))
                    if candidate_re < 1:
                        conn.rollback()
                        cur.close()
                        conn.close()
                        return 0
                    else:
                        delete_re = delete_people_image(info_type='1',image_name=str(candidate_id))
                        if delete_re == 1:
                            closeAll(conn, cur)
                            return 1
                        elif delete_re != 1:
                            conn.rollback()
                            cur.close()
                            conn.close()
                            return 0
        elif info_type == '2':
            delete_sql = """DELETE FROM `personnel_information` WHERE `id` = %s """
            re = cur.execute(delete_sql, (candidate_id))
            if re < 1:
                conn.rollback()
                cur.close()
                conn.close()
                return 0
            else:
                delete_re = delete_people_image(info_type='2',image_name=str(candidate_id))
                if delete_re == 1:
                    closeAll(conn, cur)
                    return 1
                elif delete_re != 1:
                    conn.rollback()
                    cur.close()
                    conn.close()
                    return 0
    except Exception as erro:
        app.logger.error(erro)
        return 0

#删除图片
def delete_people_image(info_type,image_name):
    try:
        image_path = app.config['UPLOAD_FOLDER']
        names = os.listdir(image_path)
        if info_type == '1':
            for name in names:
                exits = name.rfind(image_name)
                if exits == 0:
                    os.remove(image_path + name)
                    return 1
            app.logger.error('无此侯选人图片')
            return 0
        elif info_type == '2':
            candidate_id,member_id = get_new_id(image_name)
            member_name = str(candidate_id)+'_'+str(member_id)
            for name in names:
                exits = name.rfind(member_name)
                if exits == 0:
                    os.remove(image_path + name)
                    return 1
            app.logger.error('无此团队成员图片')
            return 0
    except Exception as erro:
        app.logger.error(erro)
        return 0


#查询关联表和Facebook信息是否存在
def select_candidate_facebook(info_type, content):
    try:
        if info_type == '1':
            conn = getconn()
            cur = conn.cursor()
            must_keys = ['administrative_id', 'username', 'year', 'facebook_url']
            lost_key = []
            num = 0
            for key in must_keys:
                if content.get(key) == None or content.get(key) == '':
                    lost_key.append(key)
                    num += 1
                    if num >= len(must_keys):
                        break
            if len(lost_key) != 0:
                return "输入缺失{}数据".format(lost_key)
            elif len(lost_key) == 0:
                administrative_re = get_is_candidate(content)
                if administrative_re == 407:
                    closeAll(conn, cur)
                    app.logger.error("所输入地区代码错误")
                    return 407
                elif administrative_re != 0 and administrative_re != 407:
                    closeAll(conn, cur)
                    app.logger.error("所输入候选人已存在")
                    return 406
                elif administrative_re == 0:
                    facebook_re = select_info(content)
                    if facebook_re != 0:
                        app.logger.error("候选人facebook主页信息已存在，不用重新录入")
                        cur.close()
                        conn.close()
                        return 0
                    elif facebook_re == 0:
                        app.logger.error("候选人facebook主页信息可以进行录入")
                        return 1
        elif info_type == '2':
            return 1
    except Exception as erro:
        app.logger.error(erro)
        return 0


# 写入关联表和Facebook信息
def insert_candidate_facebook(info_type, content):
    try:
        if info_type == '1':
            conn = getconn()
            cur = conn.cursor()
            must_keys = ['administrative_id', 'username', 'year', 'facebook_url']
            lost_key = []
            num = 0
            for key in must_keys:
                if content.get(key) == None or content.get(key) == '':
                    lost_key.append(key)
                    num += 1
                    if num >= len(must_keys):
                        break
            if len(lost_key) != 0:
                return "输入缺失{}数据".format(lost_key)
            elif len(lost_key) == 0:
                administrative_id = content.get('administrative_id')
                if content.get('username') != None:
                    username = content.get('username')
                else:
                    username = content.get('administrative_name')
                year = content.get('year')
                insert_sql = """INSERT INTO `candidate` (`administrative_id`,`username`,`year`) VALUES (%s,%s,%s)"""
                try:
                    hxr_re = cur.execute(insert_sql, (administrative_id, username, year))
                    auto_id = conn.insert_id()  # 返回最新写入的id
                except Exception as erro:
                    app.logger.error(erro)
                    return 0
                if hxr_re == 0:
                    app.logger.error("候选人信息写入不成功")
                    conn.rollback()
                    cur.close()
                    conn.close()
                    return 0
                elif hxr_re == 1:
                    insert_re = insert_info(auto_id, content)
                    if insert_re == 1:
                        app.logger.error("候选人信息写入成功")
                        closeAll(conn, cur)
                        # add_administrative_infos(outo_id,)
                        return auto_id
                    else:
                        return 0
        elif info_type == '2':
            return 1
    except Exception as erro:
        app.logger.error(erro)
        return 0


# 写入候选人详细信息或者是团队成员信息
def add_administrative_infos(auto_id, info_type, content):
    conn = ''
    cur = ''
    try:
        conn = getconn()
        cur = conn.cursor()
        if (info_type == '1' and auto_id != '') and auto_id != None:
            candidate_id = ''
            if auto_id != '' or auto_id != None:
                candidate_id = auto_id
            else:
                app.logger.error("自动生成id错误")
                return 0
            name = ''
            if content.get('username') != None:
                name = content.get('username')
            else:
                name = content.get('administrative_name')
            sex = ''
            if content.get('sex') != '' or content.get('sex') != None:
                sex = content.get('sex')

            name_en = ''
            if content.get('name_en') != '':
                name_en = content.get('name_en')

            birthday = ''
            if content.get('birthday') != '':
                birthday = content.get('birthday'),

            birthplace = ''
            if content.get('birthplace') != '':
                birthplace = content.get('birthplace')

            taiwan_id = ''
            if content.get('taiwan_id') != '':
                taiwan_id = content.get('taiwan_id')

            passport = ''
            if content.get('passport') != '':
                passport = content.get('passport')

            personal_webpage = ''
            if content.get('personal_webpage') != '':
                personal_webpage = content.get('personal_webpage')

            personal_phone = ''
            if content.get('personal_phone') != '':
                personal_phone = content.get('personal_phone')

            work_phone = ''
            if content.get('work_phone') != '':
                work_phone = content.get('work_phone')

            email = ''
            if content.get('email') != '':
                email = content.get('email')

            address = ''
            if content.get('address') != '':
                address = content.get('address')

            education = ''
            if content.get('education') != '':
                education = content.get('education')

            job = ''
            if content.get('job') != '':
                job = content.get('job')

            department = ''
            if content.get('department') != '':
                department = content.get('department')

            family = ''
            if content.get('family') != '':
                family = content.get('family')

            job_manager = ''
            if content.get('job_manager') != '':
                job_manager = content.get('job_manager')

            political = ''
            if content.get('political') != '':
                political = content.get('political')

            society = ''
            if content.get('society') != '':
                society = content.get('society')

            competition = ''
            if content.get('competition') != '':
                competition = content.get('competition')

            situation = ''
            if content.get('situation') != '':
                situation = content.get('situation')

            partisan = ''
            if content.get('partisan') != '':
                partisan = content.get('partisan')

            stain = ''
            if content.get('stain') != '':
                stain = content.get('stain')

            insert_houxuanren_sql = """INSERT INTO `candidate_personnel_information` (`candidate_id`,`name`,`sex`,`name_en`,`birthday`, `birthplace`,`taiwan_id`,`passport`,`personal_webpage`,`personal_phone`,`work_phone`,`email`,`address`,`education`,`job`,`department`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`partisan`,`stain`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            try:
                hxr_infos_re = cur.execute(insert_houxuanren_sql, (
                    candidate_id, name, sex, name_en, birthday, birthplace, taiwan_id, passport, personal_webpage,
                    personal_phone, work_phone, email, address, education, job, department, family, job_manager,
                    political,
                    society, competition, situation, partisan, stain))
            except Exception as erro:
                app.logger.error('写入候选人信息错误')
                conn.rollback()
                cur.close()
                conn.close()
                app.logger.error(erro)
                return 0
            if hxr_infos_re != 0:
                app.logger.error("写入候选人信息成功")
                closeAll(conn, cur)
                return auto_id
            elif hxr_infos_re == 0:
                app.logger.error('写入候选人信息错误')
                conn.rollback()
                cur.close()
                conn.close()
                return 0
        elif (info_type == '2' and auto_id != '') and auto_id != None:
            candidate_id = ''
            if content.get('candidate_id') != '' and content.get('candidate_id') != None:
                candidate_id = content.get('candidate_id')
            else:
                app.logger.error("输入所属团队领导人标识")
                return 0
            name = ''
            if content.get('name') != '' and content.get('name') != None:
                name = content.get('name')

            sex = ''
            if content.get('sex') != '' and content.get('sex') != None:
                sex = content.get('sex')

            name_en = ''
            if content.get('name_en') != '' and content.get('name_en') != None:
                name_en = content.get('name_en')

            birthday = ''
            if content.get('birthday') != '':
                birthday = content.get('birthday')

            birthplace = ''
            if content.get('birthplace') != '' and content.get('birthplace') != None:
                birthplace = content.get('birthplace')

            taiwan_id = ''
            if content.get('taiwan_id') != '' and content.get('taiwan_id') != None:
                taiwan_id = content.get('taiwan_id')

            passport = ''
            if content.get('passport') != '' and content.get('passport') != None:
                passport = content.get('passport')

            personal_webpage = ''
            if content.get('personal_webpage') != '' and content.get('personal_webpage') != None:
                personal_webpage = content.get('personal_webpage')

            personal_phone = ''
            if content.get('personal_phone') != '' and content.get('personal_phone') != None:
                personal_phone = content.get('personal_phone')

            work_phone = ''
            if content.get('work_phone') != '' and content.get('work_phone') != None:
                work_phone = content.get('work_phone')

            email = ''
            if content.get('email') != '' and content.get('email') != None:
                email = content.get('email')

            address = ''
            if content.get('address') != '' and content.get('address') != None:
                address = content.get('address')

            education = ''
            if content.get('education') != '' and content.get('education') != None:
                education = content.get('education')

            job = ''
            if content.get('job') != '' and content.get('job') != None:
                job = content.get('job')

            department = ''
            if content.get('department') != '' and content.get('department') != None:
                department = content.get('department')

            family = ''
            if content.get('family') != '' and content.get('family') != None:
                family = content.get('family')

            job_manager = ''
            if content.get('job_manager') != '' and content.get('job_manager') != None:
                job_manager = content.get('job_manager')

            political = ''
            if content.get('political') != '' and content.get('political') != None:
                political = content.get('political')

            society = ''
            if content.get('society') != '' and content.get('society') != None:
                society = content.get('society')

            competition = ''
            if content.get('competition') != '' and content.get('competition') != None:
                competition = content.get('competition')

            situation = ''
            if content.get('situation') != '' and content.get('situation') != None:
                situation = content.get('situation')

            partisan = ''
            if content.get('partisan') != '' and content.get('partisan') != None:
                partisan = content.get('partisan')

            stain = ''
            if content.get('stain') != '' and content.get('stain') != None:
                stain = content.get('stain')
            conn = getconn()
            cur = conn.cursor()
            select_sql = ''
            if birthday != '' and birthday != None:
                select_sql = """SELECT * FROM  `personnel_information` WHERE `candidate_id` = %s AND `name` = %s AND `sex` = %s AND `name_en` = %s AND `birthday` = %s AND  `birthplace` = %s AND `taiwan_id` = %s AND `passport` = %s AND `personal_webpage` = %s AND `personal_phone` = %s AND `work_phone` = %s AND `email` = %s AND `address` = %s AND `education` = %s AND `job` = %s AND `department` = %s AND `family` = %s AND `job_manager` = %s AND `political` = %s AND `society` = %s AND `competition` = %s AND `situation` = %s AND `partisan` = %s AND `stain` = %s"""
            else:
                select_sql = """SELECT * FROM  `personnel_information` WHERE `candidate_id` = %s AND `name` = %s AND `sex` = %s AND `name_en` = %s AND `birthday` IS %s AND  `birthplace` = %s AND `taiwan_id` = %s AND `passport` = %s AND `personal_webpage` = %s AND `personal_phone` = %s AND `work_phone` = %s AND `email` = %s AND `address` = %s AND `education` = %s AND `job` = %s AND `department` = %s AND `family` = %s AND `job_manager` = %s AND `political` = %s AND `society` = %s AND `competition` = %s AND `situation` = %s AND `partisan` = %s AND `stain` = %s"""
            member_re = cur.execute(select_sql, (
                candidate_id, name, sex, name_en, birthday, birthplace, taiwan_id, passport, personal_webpage,
                personal_phone, work_phone, email, address, education, job, department, family, job_manager, political,
                society, competition, situation, partisan, stain))
            if member_re != 0:
                app.logger.error("该成员信息已存在")
                return 406
            elif member_re == 0:
                insert_sql = """INSERT INTO `personnel_information` (`candidate_id`,`name`,`sex`,`name_en`,`birthday`, `birthplace`,`taiwan_id`,`passport`,`personal_webpage`,`personal_phone`,`work_phone`,`email`,`address`,`education`,`job`,`department`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`partisan`,`stain`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                re = cur.execute(insert_sql, (
                    candidate_id, name, sex, name_en, birthday, birthplace, taiwan_id, passport, personal_webpage,
                    personal_phone, work_phone, email, address, education, job, department, family, job_manager,
                    political,
                    society, competition, situation, partisan, stain))
                if re != 0:
                    app.logger.error("成员信息写入成功")
                    closeAll(conn, cur)
                    return 1
                elif re == 0:
                    app.logger.error("成员信息未记录")
                    closeAll(conn, cur)
                    return 0
    except Exception as erro:
        conn.rollback()
        cur.close()
        conn.close()
        app.logger.error(erro)
        return 0

#写入图片名称
def update_image_name(info_type,image_name,ids):
    if image_name == '' or image_name == None:
        app.logger.error('图片名称为空')
        return 0
    if ids == '' or ids == None:
        app.logger.error('图片id为空')
        return 0
    if info_type == '1':
        update_sql = """UPDATE `candidate_personnel_information` SET `image_name` = %s WHERE `candidate_id` = %s"""
        conn = getconn()
        cur = conn.cursor()
        update_re = cur.execute(update_sql,(image_name,ids))
        if update_re == 1:
            app.logger.error('侯选人图片名称写入成功')
            return 1
        else:
            app.logger.error('侯选人图片名称写入错误')
            return 0
    elif info_type == '2':
        update_sql = """UPDATE `personnel_information` SET `image_name` = %s WHERE `id` = %s"""
        conn = getconn()
        cur = conn.cursor()
        update_re = cur.execute(update_sql,(image_name,ids))
        if update_re == 1:
            app.logger.error('团队成员图片名称写入成功')
            return 1
        else:
            app.logger.error('团队成员图片名称写入错误')
            return 0

# 更新候选人信息和团队人员信息
def update_people_information(info_type, content):
    try:
        where_dict = content.get('where_dict')
        up_dict = content.get('up_dict')
        if len(where_dict) == 0 or len(up_dict) == 0:
            if len(where_dict) == 0:
                app.logger.error("更新条件不能为空")
                return 0
            if len(up_dict) == 0:
                app.logger.error("更新内容不能为空")
                return 0
        if info_type == '1':
            conn = getconn()
            cur = conn.cursor()
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

            update_sql = """UPDATE `candidate_personnel_information` SET """ + up_sql + ' WHERE ' + where_sql
            try:
                re = cur.execute(update_sql)
                if re < 1:
                    app.logger.error("候选人信息未更新")
                    return 0
                else:
                    app.logger.error("候选人信息更新成功")
                    return 1
            except Exception as erro:
                app.logger.error(erro)
                return 0
            finally:
                closeAll(conn, cur)
        elif info_type == '2':
            conn = getconn()
            cur = conn.cursor()
            up_sql = ''
            up_num = 0
            ids = ''
            if where_dict.get('id') != None:
                ids = where_dict.get('id')
            else:
                ids = where_dict.get('candidate_id')
            for k, v in up_dict.items():
                up_num += 1
                if up_num < len(up_dict):
                    up_sql += "{} = '{}', ".format(k, v)
                else:
                    up_sql += "{} = '{}' ".format(k, v)

            update_sql = """UPDATE `personnel_information` SET """ + up_sql + ' WHERE  `id` = %s'
            try:
                re = cur.execute(update_sql, (ids))
                if re < 1:
                    app.logger.error("团队成员信息未更新")
                    return 0
                else:
                    app.logger.error("团队成员信息更新成功")
                    return 1
            except Exception as erro:
                app.logger.error(erro)
                return 0
            finally:
                closeAll(conn, cur)
    except Exception as erro:
        app.logger.error(erro)
        return 0


# 获取每一个人的详细信息加上every条件后可以返回所有
def get_everyinformation(type, content):
    try:
        select_admini_name()
        if type == '1':
            result_list = []
            id = content.get('id')
            one_leader_sql = """SELECT `job`,`department`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`stain`,`sex`,`name_en`,`birthday`,`birthplace`,`taiwan_id`,`passport`,`personal_webpage`,`personal_phone`,`work_phone`,`email`,`address`,`education`,`partisan`,`name`,`candidate_id`,`year`,`administrative_id`,`image_name` FROM (SELECT * FROM `candidate_personnel_information` WHERE `candidate_id` = %s )a ,(SELECT `year`,`candidate_id` as ids,`administrative_id` FROM `candidate` WHERE `candidate_id` = %s)b WHERE a.candidate_id = b.ids """
            all_leader_sql = """SELECT `job`,`department`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`stain`,`sex`,`name_en`,`birthday`,`birthplace`,`taiwan_id`,`passport`,`personal_webpage`,`personal_phone`,`work_phone`,`email`,`address`,`education`,`partisan`,`name`,`candidate_id`,`year`,`administrative_id`,`image_name` FROM(SELECT * FROM `candidate_personnel_information` )a ,(SELECT `year`,`candidate_id` as ids,`administrative_id`  FROM `candidate` )b WHERE a.candidate_id = b.ids ORDER BY `year` DESC """
            area_all_leader_sql = """SELECT `job`,`department`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`stain`,`sex`,`name_en`,`birthday`,`birthplace`,`taiwan_id`,`passport`,`personal_webpage`,`personal_phone`,`work_phone`,`email`,`address`,`education`,`partisan`,`name`,`candidate_id`,`year`,`administrative_id`,`image_name` FROM(SELECT * FROM `candidate_personnel_information` )a ,(SELECT `year`,`candidate_id` as ids,`administrative_id`  FROM `candidate` )b WHERE a.candidate_id = b.ids AND `administrative_id` = %s ORDER BY `year` DESC """
            conn = getconn()
            cur = conn.cursor()
            every = content.get('every')
            if every == '0':
                cur.execute(one_leader_sql, (id, id))
            elif every == '1':
                cur.execute(all_leader_sql)
            else:
                cur.execute(area_all_leader_sql,(every))
            result = cur.fetchall()
            for item in result:
                leader_infos_dict = {}
                information = {}
                leader_infos_dict['image_name'] = item[26]
                leader_infos_dict['administrative_id'] = admini_id_name[item[25]]
                leader_infos_dict['year'] = item[24]
                leader_infos_dict['auto_id'] = item[23]
                leader_infos_dict['name'] = item[22]
                leader_infos_dict['job'] = item[0]
                leader_infos_dict['department'] = item[1]
                leader_infos_dict['family'] = item[2]
                leader_infos_dict['job_manager'] = item[3]
                leader_infos_dict['political'] = item[4]
                leader_infos_dict['society'] = item[5]
                leader_infos_dict['competition'] = item[6]
                leader_infos_dict['situation'] = item[7]
                leader_infos_dict['stain'] = item[8]
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
                leader_infos_dict['information'] = information
                result_list.append(leader_infos_dict)
            closeAll(conn, cur)
            return result_list

        elif type == '2':
            id = ''
            candidate_id = content.get('candidate_id')
            if content.get('id') == None:
                id = content.get('candidate_id')
            conn = getconn()
            cur = conn.cursor()
            every = content.get('every')
            member_sql = """SELECT `job`,`department`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`stain`,`sex`,`name_en`,`birthday`,`birthplace`,`taiwan_id`,`passport`,`personal_webpage`,`personal_phone`,`work_phone`,`email`,`address`,`education`,`partisan`,`id`,`name`,`candidate_id`,`year`,`administrative_id`,`image_name` FROM(SELECT * FROM `personnel_information` WHERE `id` = %s)a, (SELECT `year`,`candidate_id` as ids,`administrative_id` FROM `candidate` WHERE `candidate_id` = (SELECT `candidate_id` FROM `personnel_information` WHERE `id` = %s ))b WHERE a.candidate_id = b.ids """
            all_member_sql = """SELECT `job`,`department`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`stain`,`sex`,`name_en`,`birthday`,`birthplace`,`taiwan_id`,`passport`,`personal_webpage`,`personal_phone`,`work_phone`,`email`,`address`,`education`,`partisan`,`id`,`name`,`candidate_id`,`year`,`administrative_id`,`image_name` FROM (SELECT * FROM `personnel_information` WHERE `candidate_id` = %s)a,(SELECT `year`,`candidate_id` as ids,`administrative_id`  FROM `candidate` WHERE `candidate_id` =%s)b  WHERE a.candidate_id = b.ids """
            count = ''
            if every == '0':
                count = cur.execute(member_sql, (id, id))
            elif every == '1':
                cur.execute(all_member_sql, (candidate_id, candidate_id))
            if count != 0:
                result = cur.fetchall()

                result_list = []
                for item in result:
                    member_dict = {}
                    information = {}
                    member_dict['image_name'] = item[27]
                    member_dict['administrative_id'] = admini_id_name[item[26]]
                    member_dict['year'] = item[25]
                    member_dict['candidate_id'] = item[24]
                    member_dict['name'] = item[23]
                    member_dict['auto_id'] = item[22]
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
                    result_list.append(member_dict)
                closeAll(conn, cur)
                return result_list
            else:
                closeAll(conn, cur)
                app.logger.error("查无此人员信息")
                return 0
        else:
            app.logger.error("传入正确的类型")
            return 0
    except Exception as erro:
        app.logger.error(erro)
        return 0


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


# 做分页
def get_pages():
    conn = getconn()
    cur = conn.cursor()
    try:
        all_leader_sql = """SELECT `job`,`department`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`stain`,`sex`,`name_en`,`birthday`,`birthplace`,`taiwan_id`,`passport`,`personal_webpage`,`personal_phone`,`work_phone`,`email`,`address`,`education`,`partisan`,`name`,`candidate_id`,`year`,`administrative_id` FROM(SELECT * FROM `candidate_personnel_information` )a ,(SELECT `year`,`candidate_id` as ids,`administrative_id`  FROM `candidate` )b WHERE a.candidate_id = b.ids ORDER BY `year` DESC """
        count = cur.execute(all_leader_sql)
        if count < 1:
            return 0
        else:
            return count
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 校验图片是否正确
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 获取最新写入的侯选人或者是团队人员的id
def get_new_id(info_type):
    conn = getconn()
    cur = conn.cursor()
    try:
        if info_type == '1':
            leader_id_sql = """SELECT `candidate_id` FROM `candidate` ORDER BY  `candidate_id` DESC  LIMIT 1"""
            leader_re = cur.execute(leader_id_sql)
            if leader_re == 0:
                app.logger.error('无此候选人信息')
                return 0
            re_id = cur.fetchone()
            return re_id[0]
        elif info_type == '2':
            leader_member_id_sql = """SELECT `candidate_id`,`id` FROM `personnel_information` ORDER BY  `id` DESC  LIMIT 1"""
            member_re = cur.execute(leader_member_id_sql)
            if member_re == 0:
                app.logger.error('无此团队成员信息')
                return 0
            re_id = cur.fetchone()
            return re_id[0], re_id[1]
        else:
            delete_member_id_sql = """SELECT `candidate_id`,`id` FROM `personnel_information` WHERE `id` = %s"""
            delete_re = cur.execute(delete_member_id_sql,(info_type))
            if delete_re == 0:
                app.logger.error('无次团队成员信息')
                return 0
            re_id = cur.fetchone()
            return re_id[0], re_id[1]
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


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