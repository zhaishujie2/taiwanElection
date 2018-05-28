# coding=utf-8
from monitor.util.mysql_util import getconn, closeAll
from collections import OrderedDict
from monitor import app


# 获取每个候选人团队信息
def get_party(message):
    try:
        every_list = []
        for name_id, name in message.items():
            leader_dict = OrderedDict()
            member_list = []
            houxuanren_sql = """SELECT `partisan` FROM candidate_personnel_information WHERE `candidate_id`= %s"""
            member_sql = """SELECT `name`,`job`,`department`,`id` FROM personnel_information WHERE `candidate_id` = %s"""
            houxuanren_conn = getconn()
            houxuanren_cur = houxuanren_conn.cursor()
            member_conn = getconn()
            member_cur = member_conn.cursor()
            houxuanren_cur.execute(houxuanren_sql,(name_id))
            member_cur.execute(member_sql,(name_id))
            members = member_cur.fetchall()
            party = houxuanren_cur.fetchone()
            for member in members:
                member_dict = {}
                member_dict['name'] = member[0]
                member_dict['job'] = member[1]
                member_dict['department'] = member[2]
                member_dict['id'] = member[3]
                member_list.append(member_dict)
            leader_dict['name'] = name
            leader_dict['id'] = name_id
            leader_dict['party'] = party[0]
            leader_dict['member'] = member_list
            every_list.append(leader_dict)
            closeAll(houxuanren_conn, houxuanren_cur)
            closeAll(member_conn, member_cur)
        return every_list
    except Exception as erro:
        app.logger.error(erro)
        return str(erro)


# 获取每一个人的详细信息
def get_everyinformation(type, content):
    try:
        if type == '1' and len(content) == 1:
            result_list = []
            id = content.get('id')
            leader_infos_dict = {}
            information = {}
            leader_sql = """SELECT `job`,`department`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`stain`,`sex`,`name_en`,`birthday`,`birthplace`,`taiwan_id`,`passport`,`personal_webpage`,`personal_phone`,`work_phone`,`email`,`address`,`education`,`partisan` FROM `candidate_personnel_information` WHERE  `candidate_id` = %s"""
            conn = getconn()
            cur = conn.cursor()
            cur.execute(leader_sql, (id))
            result = cur.fetchall()
            for item in result:
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

        elif type == '2' and len(content) == 2:
            keys_list = []
            for item in content.keys():
                keys_list.append(item)
            id = content.get('id')
            name = content.get('name')
            conn = getconn()
            cur = conn.cursor()
            member_sql = """SELECT `job`,`department`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`stain`,`sex`,`name_en`,`birthday`,`birthplace`,`taiwan_id`,`passport`,`personal_webpage`,`personal_phone`,`work_phone`,`email`,`address`,`education`,`partisan` FROM `personnel_information` WHERE `id` = %s AND `name` = %s"""
            count = cur.execute(member_sql, (id, name))
            if count != 0:
                result = cur.fetchall()
                member_dict = {}
                information = {}
                result_list = []
                for item in result:
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
                app.logger.error("查无此人")
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

#获取历届选举人情况
def get_all_candidate_infos(region,year):
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
        cur.execute(select_id_sql,(region))
        id_item = cur.fetchone()
        if id_item[0] != None and id_item[0] != '':
            select_sql = """SELECT `administrative_id`,`elector`,`election_score`,`election_parties`,`period`,`year` FROM `previous_elections` WHERE year < %s AND  (`administrative_id` = %s OR `administrative_id` = %s) GROUP BY `administrative_id`,`year`,`elector`,`election_parties`,`period` ORDER BY `period` ASC,administrative_id DESC,election_score DESC """
            try:
                cur.execute(select_sql,(year,region,id_item[0]))
            except Exception as erro:
                app.logger.error(erro)
                closeAll(conn,cur)
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
            closeAll(conn,cur)
            end_list = [{"elections":infos_list,"area":dict_list}]
            return end_list
        else:
            select_sql = """SELECT `administrative_id`,`elector`,`election_score`,`election_parties`,`period`,`year` FROM `previous_elections` WHERE year < %s AND  `administrative_id` = %s GROUP BY `administrative_id`,`year`,`elector`,`election_parties`,`period` ORDER BY `period` ASC,administrative_id DESC,election_score DESC """
            try:
                cur.execute(select_sql,(year,region))
            except Exception as erro:
                app.logger.error(erro)
                closeAll(conn,cur)
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
            closeAll(conn,cur)
            end_list = [{"elections":infos_list,"area":dict_list}]
            return end_list
    except Exception as erro:
        app.logger.error(erro)
        return 0
# if __name__ == '__main__':
# print (get_gov_area(7017,2018))
# message = {"1": "卢秀燕", "2": "林佳龙"}
# get_party(message)
#     # content = {"id":"1"}
#     content = {"id":"1","name":"小白","department":"13局","job":"部长"}
#     get_everyinformation('2',content)
