# coding=utf-8
from monitor.util.mysql_util import getconn, closeAll
from collections import OrderedDict
from monitor import app
from flask import session
from monitor.util.config import IP

# 获取每个候选人团队信息
def get_party(message):
    try:
        every_list = []
        infos_dict = {}
        member_list = ''
        houxuanren_conn = ''
        houxuanren_cur = ''
        member_conn = ''
        member_cur = ''
        end_links_list = []
        for name_id, name in message.items():
            leader_dict = OrderedDict()
            houxuanren_sql = """SELECT `partisan`,`image_name`FROM `candidate_personnel_information` WHERE `candidate_id`= %s"""
            member_sql = """SELECT `name`,`job`,`department`,`id`,`image_name` FROM `personnel_information` WHERE `candidate_id` = %s"""
            houxuanren_conn = getconn()
            houxuanren_cur = houxuanren_conn.cursor()
            member_conn = getconn()
            member_cur = member_conn.cursor()
            houxuanren_cur.execute(houxuanren_sql, (name_id))
            member_cur.execute(member_sql, (name_id))
            members = member_cur.fetchall()
            party = houxuanren_cur.fetchone()
            member_list = []

            for member in members:
                member_dict = {}
                member_dict['name'] = member[0]
                member_dict['job'] = member[1]
                member_dict['department'] = member[2]
                member_dict['team_id'] = member[3]
                member_dict['type'] = 2
                if member[4] != '':
                    member_dict['symbol'] = "image://http://"+IP+"/"+member[4]

                else:
                    member_dict['symbol'] = "image://http://"+IP+"/unknown.png"
                member_dict['symbolSize'] = [70,70]
                member_dict['draggable'] = 'false'
                member_dict['category'] = 1
                member_dict['label'] = {
                    'verticalAlign':'bottom',
                    'offset':[5,55],
                    'fontStyle':'normal',
                    'color': 'auto',
                    'fontSize': 16,
                }
                member_list.append(member_dict)
            leader_dict['name'] = name
            leader_dict['type'] = 1
            leader_dict['category'] = 0
            leader_dict['team_id'] = int(name_id)
            leader_dict['party'] = party[0]
            if party[1] != '':
                leader_dict['symbol'] = "image://http://"+IP+"/"+ party[1]
            else:
                leader_dict['symbol'] = "image://http://"+IP+"/unknown.png"
            leader_dict['symbolSize'] = [70,70]
            leader_dict['label'] = {
                'verticalAlign':'bottom',
                'offset':[5,55],
                'fontStyle':'normal',
                'color': 'auto',
                'fontSize': 16,
            }
            leader_dict['draggable'] = 'true'
            mid_leader_dict = {}
            mid_leader_dict['member'] = member_list
            mid_leader_dict['name'] = leader_dict['name']
            mid_links_list = get_links(mid_leader_dict)
            end_links_dic = {}
            end_links_dic[leader_dict['name']] = mid_links_list
            end_links_list.append(end_links_dic)
            if party[0] in infos_dict.keys():
                mids_list = infos_dict[party[0]]
                mids_list.append(leader_dict)
                for mem in member_list:
                    mids_list.append(mem)
                infos_dict[party[0]] = mids_list
            else:
                leader_dict['name'] = name
                leader_dict['team_id'] = int(name_id)
                leader_dict['party'] = party[0]
                mid_list = [leader_dict]
                for mem in member_list:
                    mid_list.append(mem)
                infos_dict[party[0]] = mid_list
        every_list.append(infos_dict)
        end_list = []
        end_dic = OrderedDict()
        keys_list = list(every_list[0].keys())
        all_keys_list = list(every_list[0].keys())
        keys_num = len(keys_list)
        if '民进党' in keys_list:
            keys_list.remove('民进党')
        else:
            pass
        if '国民党' in keys_list:    
            keys_list.remove('国民党')
        else:
            pass
        num_dic = OrderedDict()
        for item in every_list:
            if '民进党' in all_keys_list:
                mid_dic = {}
                mid_dic['data'] = item['民进党']
                one_links = get_one_links(item,'民进党',end_links_list)
                mid_dic['links'] = one_links
                end_dic['民进党'] = mid_dic
            else:
                pass
            if '国民党' in all_keys_list:
                mid_dic ={}
                mid_dic['data'] = item['国民党']
                one_links = get_one_links(item,'国民党',end_links_list)
                mid_dic['links'] = one_links
                end_dic['国民党'] = mid_dic
            else:
                pass
            for key in keys_list:
                mid_dic={}
                mid_dic['data'] = item[key]
                one_links = get_one_links(item,key,end_links_list)
                mid_dic['links'] = one_links
                end_dic[key] = mid_dic
            num_dic = {}
            num = -1
            for k,v in end_dic.items():
                if k == '民进党':
                    zhuan_dic = {}
                    zhuan_dic[k]=v
                    num_dic['0'] = zhuan_dic
                elif k == '国民党':
                    zhuan_dic = {}
                    zhuan_dic[k]=v
                    num_dic['1'] = zhuan_dic
                elif k == '无党':
                    zhuan_dic = {}
                    zhuan_dic[k]=v
                    num_dic[str(keys_num)] = zhuan_dic
                else:

                    zhuan_dic = {}
                    zhuan_dic[k]=v
                    if keys_num > 2:
                        num_dic[str(keys_num+num)] = zhuan_dic
                    elif keys_num <= 2:
                        num_dic[str(3+num)] = zhuan_dic
                    num -= 1
        end_list.append(num_dic)
        closeAll(houxuanren_conn, houxuanren_cur)
        closeAll(member_conn, member_cur)
        return end_list
    except Exception as erro:
        app.logger.error(erro)
        return str(erro)

#将每一个links添加到links中
def get_one_links(item,dangpai,end_links_list):
    all_links_list = []
    for na in item[dangpai]:
        leader_name = na['name']
        if na['type'] == 1:
            for links in end_links_list:
                if links.get(leader_name) == None:
                    pass
                elif links.get(leader_name) != None:
                    for one in links[leader_name]:
                        all_links_list.append(one)
    return all_links_list

#获得每个以后选人的links
def get_links(leader_dic):
    end_links_list = []
    target_list = []
    links_dic = {}
    for one in leader_dic['member']:
        links_dic['source'] = leader_dic['name']
        if one['type'] == 2:
            links_dic['target'] = one['name']
            target_list.append(one['name'])
    for tar in target_list:
        end_links = {}
        end_links['source'] = links_dic['source']
        end_links['target'] = tar
        end_links['value'] = ''
        end_links_list.append(end_links)
    return end_links_list

# 获取每一个人的详细信息加上every条件后可以返回所有
def get_everyinformation(type, content):
    try:
        if type == '1':
            result_list = []
            id = content.get('id')
            one_leader_sql = """SELECT `job`,`department`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`stain`,`sex`,`name_en`,`birthday`,`birthplace`,`taiwan_id`,`passport`,`personal_webpage`,`personal_phone`,`work_phone`,`email`,`address`,`education`,`partisan`,`name`,`candidate_id`,`mainland_pass`,`character_feature`,`social_activity`,`asset_status`,`image_infos` FROM `candidate_personnel_information` WHERE  `candidate_id` = %s"""
            all_leader_sql = """SELECT `job`,`department`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`stain`,`sex`,`name_en`,`birthday`,`birthplace`,`taiwan_id`,`passport`,`personal_webpage`,`personal_phone`,`work_phone`,`email`,`address`,`education`,`partisan`,`name`,`candidate_id`,`mainland_pass`,`character_feature`,`social_activity`,`asset_status`,`image_infos` FROM `candidate_personnel_information`"""
            conn = getconn()
            cur = conn.cursor()
            every = content.get('every')
            if every == '0':
                cur.execute(one_leader_sql, (id))
            elif every == '1':
                cur.execute(all_leader_sql)
            # result = cur.fetchmany()
            result = cur.fetchall()
            for item in result:
                leader_infos_dict = {}
                information = {}
                leader_infos_dict['social_activity'] = item[26]
                leader_infos_dict['asset_status'] = item[27]
                leader_infos_dict['image_infos'] = item[28]
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
                information['mainland_pass'] = item[24]
                information['character_feature'] = item[25]
                leader_infos_dict['information'] = information
                result_list.append(leader_infos_dict)
            closeAll(conn, cur)
            return result_list

        elif type == '2':
            candidate_id = content.get('candidate_id')
            id = content.get('id')
            conn = getconn()
            cur = conn.cursor()
            member_sql = """SELECT `job`,`department`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`stain`,`sex`,`name_en`,`birthday`,`birthplace`,`taiwan_id`,`passport`,`personal_webpage`,`personal_phone`,`work_phone`,`email`,`address`,`education`,`partisan`,`id`,`name`,`candidate_id`,`mainland_pass`,`character_feature`,`social_activity`,`asset_status`,`image_infos` FROM `personnel_information` WHERE `id` = %s """
            all_member_sql = """SELECT `job`,`department`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`stain`,`sex`,`name_en`,`birthday`,`birthplace`,`taiwan_id`,`passport`,`personal_webpage`,`personal_phone`,`work_phone`,`email`,`address`,`education`,`partisan`,`id`,`name`,`candidate_id`,`mainland_pass`,`character_feature`,`social_activity`,`asset_status`,`image_infos` FROM `personnel_information` WHERE `candidate_id` = %s"""
            every = content.get('every')
            count = ''
            if every == '0':
                count = cur.execute(member_sql, (id))
            elif every == '1':
                cur.execute(all_member_sql, (candidate_id))
            if count != 0:
                result = cur.fetchall()

                result_list = []
                for item in result:
                    member_dict = {}
                    information = {}
                    member_dict['social_activity'] = item[27]
                    member_dict['asset_status'] = item[28]
                    member_dict['image_infos'] = item[29]
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
                    information['mainland_pass'] = item[25]
                    information['character_feature'] = item[26]
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


# 获取地区信息
def get_gov_area(id, year):
    conn = getconn()
    cur = conn.cursor()
    info_dict = {}
    try:
        sql = "SELECT area_info,governance_situation FROM administrative_infos WHERE administrative_id = %s and `year` = %s"
        re = cur.execute(sql, (id, year))
        if re < 1:
            return {}
        else:
            result = cur.fetchone()
            info_dict['area_info'] = result[0]
            info_dict['gov'] = result[1]
            return info_dict
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 获取历届选举人情况
def get_all_candidate_infos(region, year):
    try:
        conn = getconn()
        cur = conn.cursor()
        select_dict_sql = """SELECT `administrative_id`,`administrative_name` FROM `administrative_area`"""
        cur.execute(select_dict_sql)
        dict_re = cur.fetchall()
        dict_list = []
        dict_dict = {}
        for item in dict_re:
            dict_dict[str(item[0])] = item[1]
        dict_list.append(dict_dict)
        select_id_sql = """SELECT `regional_consolidation` FROM `administrative_area` WHERE `administrative_id` = %s"""
        cur.execute(select_id_sql, (region))
        id_item = cur.fetchone()
        if id_item[0] != None and id_item[0] != '':
            select_sql = """SELECT `administrative_id`,`elector`,`election_score`,`election_parties`,`period`,`year` FROM `previous_elections` WHERE year < %s AND  (`administrative_id` = %s OR `administrative_id` = %s) GROUP BY `administrative_id`,`year`,`elector`,`election_parties`,`period` ORDER BY `period` ASC,administrative_id DESC,election_score DESC """
            try:
                cur.execute(select_sql, (year, region, id_item[0]))
            except Exception as erro:
                app.logger.error(erro)
                closeAll(conn, cur)
                return 0
            other_results = cur.fetchall()
            infos_list = []
            for item in other_results:
                infos_dict = {}
                infos_dict['administrative_id'] = item[0]
                infos_dict['elector'] = item[1]
                infos_dict['election_score'] = item[2]
                infos_dict['election_parties'] = item[3]
                infos_dict['period'] = item[4]
                infos_dict['year'] = item[5]
                infos_list.append(infos_dict)
            closeAll(conn, cur)
            end_list = [{"elections": infos_list, "area": dict_list}]
            return end_list
        else:
            select_sql = """SELECT `administrative_id`,`elector`,`election_score`,`election_parties`,`period`,`year` FROM `previous_elections` WHERE year < %s AND  `administrative_id` = %s GROUP BY `administrative_id`,`year`,`elector`,`election_parties`,`period` ORDER BY `period` ASC,administrative_id DESC,election_score DESC """
            try:
                cur.execute(select_sql, (year, region))
            except Exception as erro:
                app.logger.error(erro)
                closeAll(conn, cur)
                return 0
            results = cur.fetchall()
            infos_list = []
            for item in results:
                infos_dict = {}
                infos_dict['administrative_id'] = item[0]
                infos_dict['elector'] = item[1]
                infos_dict['election_score'] = item[2]
                infos_dict['election_parties'] = item[3]
                infos_dict['period'] = item[4]
                infos_dict['year'] = item[5]
                infos_list.append(infos_dict)
            closeAll(conn, cur)
            end_list = [{"elections": infos_list, "area": dict_list}]
            return end_list
    except Exception as erro:
        app.logger.error(erro)
        return 0
