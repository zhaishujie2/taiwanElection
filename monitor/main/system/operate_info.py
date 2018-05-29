# coding=utf-8
from monitor.util.mysql_util import getconn,closeAll
from monitor import app
from flask import session

#facebook写入数据
def insert_info(auto_id,datas):
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
        # print(insert_sql)
        insert_re = ''
        select_re = cur.execute(select_sql,(administrative_id,administrative_name,year,facebook_url))
        if select_re != 0:
            return 406
        elif select_re == 0:
            insert_re = cur.execute(insert_sql,(auto_id,administrative_id,administrative_name,year,facebook_url))
        # print(re)
        if insert_re < 1:
            return 0
        else:
            return 1
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn,cur)

#facebook删除数据
def delete_info(data):
    conn = getconn()
    cur = conn.cursor()
    ids = data.get('candidate_id')
    try:
        delete_sql = """DELETE FROM `spider_infos` WHERE id = %s """
        re = cur.execute(delete_sql,(ids))
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
        closeAll(conn,cur)

#facebook修改数据
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
                return 0
            else:
                return 1
        except Exception as erro:
            app.logger.error(erro)
            return 0
        finally:
            closeAll(conn,cur)

#facebook查询数据
def select_info(datas):
    conn = getconn()
    cur = conn.cursor()
    try:
        where_sql = ''
        num = 0
        for k,v in datas.items():
            if k == 'username':
                k = 'administrative_name'
            num += 1
            if num < len(datas):
                where_sql += "{} = '{}'".format(k,v) + ' AND '
            else:
                where_sql += "{} = '{}'".format(k,v)

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
    count = ''
    try:
        count = cur.execute(select_sql,(administrative_id,username,year))
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
    elif types == '3':#查询候选人信息
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


#删除候选人信息或者团队人员信息
def delete_people_information(type,content):
    conn = getconn()
    cur = conn.cursor()
    candidate_id = content.get('candidate_id')
    info_type = content.get('type')
    try:
        if info_type == '1':
            spider_re = delete_info(content)
            if spider_re == 1:
                delete_candidate_personnel_information_sql = """DELETE FROM `candidate_personnel_information` WHERE `candidate_id` = %s """
                delete_candidate_sql = """DELETE FROM `candidate` WHERE `candidate_id` = %s """
                information_re = cur.execute(delete_candidate_personnel_information_sql,(candidate_id))
                if information_re < 1:
                    conn.rollback()
                    cur.close()
                    conn.close()
                    return 0
                else:
                    candidate_re = cur.execute(delete_candidate_sql,(candidate_id))
                    if candidate_re < 1:
                        conn.rollback()
                        cur.close()
                        conn.close()
                        return 0
                    closeAll(conn,cur)
                    return 1
        elif info_type == '2':
            delete_sql = """DELETE FROM `personnel_information` WHERE `id` = %s """
            re = cur.execute(delete_sql,(candidate_id))
            if re < 1:
                conn.rollback()
                cur.close()
                conn.close()
                return 0
            else:
                closeAll(conn,cur)
                return 1
    except Exception as erro:
        app.logger.error(erro)
        return 0


#查询关联表和Facebook信息是否存在
def select_candidate_facebook(info_type,content):
    try:
        if info_type == '1':
            conn = getconn()
            cur = conn.cursor()
            must_keys = ['administrative_id','username','year','facebook_url']
            lost_key = []
            num = 0
            for key in must_keys:
                if content.get(key) == None or content.get(key) == '':
                    lost_key.append(key)
                    num += 1
                    if num >=len(must_keys):
                        break
            if len(lost_key) != 0:
                return "输入缺失{}数据".format(lost_key)
            elif len(lost_key) == 0:
                administrative_re = get_is_candidate(content)
                # print(count)
                if administrative_re == 407:
                    closeAll(conn,cur)
                    app.logger.error("所输入地区代码错误")
                    return 407
                elif administrative_re != 0 and administrative_re != 407:
                    closeAll(conn,cur)
                    app.logger.error("所输入候选人已存在")
                    return 406
                elif administrative_re == 0:
                    facebook_re = select_info(content)
                    if facebook_re != 0:
                        app.logger.error("候选人facebook主页信息已录入")
                        cur.close()
                        conn.close()
                        return 0
                    elif facebook_re == 0:
                        app.logger.error("候选人facebook主页信息未录入")
                        return 1
        elif info_type == '2':
            return 1
    except Exception as erro:
        app.logger.error(erro)
        return 0


#写入关联表和Facebook信息
def insert_candidate_facebook(info_type,content):
    try:
        if info_type == '1':
            conn = getconn()
            cur = conn.cursor()
            must_keys = ['administrative_id','username','year','facebook_url']
            lost_key = []
            num = 0
            for key in must_keys:
                if content.get(key) == None or content.get(key) == '':
                    lost_key.append(key)
                    num += 1
                    if num >=len(must_keys):
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
                    hxr_re = cur.execute(insert_sql,(administrative_id,username,year))
                    auto_id = conn.insert_id()#返回最新写入的id
                except Exception as erro:
                    app.logger.error(erro)
                    return 0
                if hxr_re == 0:
                    app.logger.error("候选人信息未记录")
                    conn.rollback()
                    cur.close()
                    conn.close()
                    return 0
                elif hxr_re == 1:
                        insert_re = insert_info(auto_id,content)
                        if insert_re == 1:
                            app.logger.error("候选人信息写入")
                            closeAll(conn,cur)
                            # add_administrative_infos(outo_id,)
                            return auto_id
                        else:
                            return 0
        elif info_type == '2':
            return 1
    except Exception as erro:
        app.logger.error(erro)
        return 0

#写入候选人详细信息或者是团队成员信息
def add_administrative_infos(auto_id,info_type,content):
    try:
        conn = getconn()
        cur = conn.cursor()
        if info_type =='1':
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
            if content.get('sex')!= '' or content.get('sex') != None :
                sex = content.get('sex')

            name_en = ''
            if content.get('name_en') != '':
                name_en = content.get('name_en')

            birthday = ''
            if content.get('birthday') != '':
                birthday = content.get('birthday'),

            birthplace= ''
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
                hxr_infos_re = cur.execute(insert_houxuanren_sql,(candidate_id,name,sex,name_en,birthday, birthplace,taiwan_id,passport,personal_webpage,personal_phone,work_phone,email,address,education,job,department,family,job_manager,political,society,competition,situation,partisan,stain))
            # print(re)
            except Exception as erro:
                app.logger.error(erro)
                return 0
            if hxr_infos_re != 0:
                app.logger.error("写入候选人信息成功")
                closeAll(conn,cur)
                return 1
            elif hxr_infos_re == 0:
                app.logger.erro('写入候选人信息错误')
                conn.rollback()
                cur.close()
                conn.close()
                return 0
        elif info_type == '2':
            message = session["electors"]
            key_list = []
            for key in message.keys():
                key_list.append(key)
            candidate_id = ''
            if (content.get('candidate_id') != '' and content.get('candidate_id') != None) and content.get('candidate_id') in key_list:
                candidate_id = content.get('candidate_id')
            else:
                app.logger.error("输入所属团队领导人标识")
                return 0
            name = ''
            if content.get('name') != '' and content.get('name') != None:
                name = content.get('name')

            sex = ''
            if  content.get('sex')!= '' and content.get('sex') != None:
                sex = content.get('sex')

            name_en = ''
            if content.get('name_en') != '' and content.get('name_en') != None:
                name_en = content.get('name_en')

            birthday = ''
            if content.get('birthday') != '' :
                birthday = content.get('birthday')

            birthplace= ''
            if content.get('birthplace') != '' and content.get('birthplace') != None:
                birthplace = content.get('birthplace')

            taiwan_id = ''
            if content.get('taiwan_id') != '' and content.get('taiwan_id') != None:
                taiwan_id = content.get('taiwan_id')

            passport = ''
            if content.get('passport') != '' and content.get('passport') != None:
                passport = content.get('passport')

            personal_webpage = ''
            if content.get('personal_webpage') != ''and content.get('personal_webpage') != None:
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
            member_re = cur.execute(select_sql,(candidate_id,name,sex,name_en,birthday, birthplace,taiwan_id,passport,personal_webpage,personal_phone,work_phone,email,address,education,job,department,family,job_manager,political,society,competition,situation,partisan,stain))
            if member_re != 0:
                app.logger.error("该成员信息已存在")
                return 406
            elif member_re == 0:
                insert_sql = """INSERT INTO `personnel_information` (`candidate_id`,`name`,`sex`,`name_en`,`birthday`, `birthplace`,`taiwan_id`,`passport`,`personal_webpage`,`personal_phone`,`work_phone`,`email`,`address`,`education`,`job`,`department`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`partisan`,`stain`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                re = cur.execute(insert_sql,(candidate_id,name,sex,name_en,birthday, birthplace,taiwan_id,passport,personal_webpage,personal_phone,work_phone,email,address,education,job,department,family,job_manager,political,society,competition,situation,partisan,stain))
                # print(re)
                if re != 0:
                    app.logger.error("成员信息写入成功")
                    closeAll(conn,cur)
                    return 1
                elif re == 0:
                    app.logger.error("成员信息未记录")
                    closeAll(conn,cur)
                    return 0
    except Exception as erro:
        app.logger.error(erro)
        return 0


# if __name__ == '__main__':
#     # a = insert_info('7017','李晨','2018','www.facebook.com')
#     a = delete_info(11)#{"administrative_id":"7019","administrative_name":"李晨"}
#     # a = select_info({"administrative_id":"7017","administrative_name":"李晨","year":"2018","facebook_url":"www.baidu.com"})
#     # a = update_info(up_dict={"administrative_id":"7020","administrative_name":"lichen"},where_dict={"administrative_id":"7019","administrative_name":"李晨"})
#     # a = select_info({"administrative_name":"李晨","year":"2020"})
#     print(a)


