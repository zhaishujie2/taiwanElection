# coding=utf-8
from monitor.util.mysql_util import getconn,closeAll
from collections import OrderedDict
from monitor import app
#获取每个候选人团队信息
def get_party(message):
    try:
        every_list = []
        print(type(message))
        for name_id,name in message.items():
            leader_dict = OrderedDict()
            member_list = []
            houxuanren_sql = """SELECT `partisan` FROM candidate_personnel_information WHERE `candidate_id`= '%s'"""%(name_id)
            member_sql = """SELECT `name`,`job`,`department`,`id` FROM personnel_information WHERE `candidate_id` = '%s'"""%(name_id)
            houxuanren_conn = getconn()
            houxuanren_cur = houxuanren_conn.cursor()
            member_conn = getconn()
            member_cur = member_conn.cursor()
            houxuanren_cur.execute(houxuanren_sql)
            member_cur.execute(member_sql)
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
            closeAll(houxuanren_conn,houxuanren_cur)
            closeAll(member_conn,member_cur)
        return every_list
    except Exception as erro:
        app.logger.error(erro)
        return str(erro)

#获取每一个人的详细信息
def get_everyinformation(type,content):
    try:
        if type == '1' and len(content) == 1:
            result_list = []
            id = content.get('id')
            leader_infos_dict = {}
            leader_sql = """SELECT `job`,`department`,`information`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`stain` FROM `candidate_personnel_information` WHERE  `candidate_id` = '%s'"""%(id)
            conn = getconn()
            cur = conn.cursor()
            cur.execute(leader_sql)
            result = cur.fetchall()
            for item in result:
                leader_infos_dict['job'] = item[0]
                leader_infos_dict['department'] = item[1]
                leader_infos_dict['information'] = item[2]
                leader_infos_dict['family'] = item[3]
                leader_infos_dict['job_manager'] = item[4]
                leader_infos_dict['political'] = item[5]
                leader_infos_dict['society'] = item[6]
                leader_infos_dict['competition'] = item[7]
                leader_infos_dict['situation'] = item[8]
                leader_infos_dict['stain'] = item[9]
            result_list.append(leader_infos_dict)
            closeAll(conn,cur)
            return result_list,'0'

        elif type == '2' and len(content) == 4:
            keys_list = []
            for item in content.keys():
                keys_list.append(item)
            if keys_list != ['id', 'name', 'department', 'job']:
                return "请输入正确的条件信息",'0'
            else:
                name_id = content.get('id')
                name = content.get('name')
                department = content.get('department')
                job = content.get('job')
                conn = getconn()
                cur = conn.cursor()
                member_sql = """SELECT `job`,`department`,`information`,`family`,`job_manager`,`political`,`society`,`competition`,`situation`,`stain`,`name` FROM `personnel_information` WHERE `candidate_id` = '%s' AND `name` = '%s'  AND `department` = '%s' AND `job` = '%s'"""%(name_id,name,department,job)
                print(member_sql)
                count = cur.execute(member_sql)
                if count != 0:
                    result = cur.fetchall()
                    member_dict = {}
                    result_list = []
                    for item in result:
                        member_dict['job'] = item[0]
                        member_dict['department'] = item[1]
                        member_dict['information'] = item[2]
                        member_dict['family'] = item[3]
                        member_dict['job_manager'] = item[4]
                        member_dict['political'] = item[5]
                        member_dict['society'] = item[6]
                        member_dict['competition'] = item[7]
                        member_dict['situation'] = item[8]
                        member_dict['stain'] = item[9]
                        member_dict['name'] = item[10]
                    result_list.append(member_dict)
                    closeAll(conn,cur)
                    return result_list,'1'
                else:
                    closeAll(conn,cur)
                    return "查无此人",'1'
        else:
            return "传入正确的类型",'0'
    except Exception as erro:
        app.logger.error(erro)
        return str(erro)



# if __name__ == '__main__':
#     # message = {"1": "卢秀燕", "2": "林佳龙"}
#     # get_party(message)
#     # content = {"id":"1"}
#     content = {"id":"1","name":"小白","department":"13局","job":"部长"}
#     get_everyinformation('2',content)

