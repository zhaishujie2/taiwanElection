# coding=utf-8
from monitor.util.mysql_util import getconn,closeAll
from monitor import app

def get_popular_info(date,message):
    conn = getconn()
    cur = conn.cursor()
    id_list = message.keys()
    try:
        hxr_dic = {}
        for name_id in id_list:
            sql = "SELECT CAST(`create_data` AS CHAR),`popularity_score` FROM popularity WHERE DATE_SUB('{}', INTERVAL 7 DAY) < `create_data`  AND `create_data` <= '{}' AND `candidate_id` ='{}' ORDER BY `create_data` ASC".format(date,date,name_id)
            # print(sql)
            cur.execute(sql)
            # print(count)
            result = cur.fetchall()
            every_dic = {}
            for re in result:
                every_dic[re[0]] = re[1]
            hxr_dic[message.get(name_id)] = every_dic
        return hxr_dic
    except Exception as erro:
        app.logger.error(erro)
        return "0"
    finally:
        closeAll(conn,cur)


