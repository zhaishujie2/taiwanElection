# coding=utf-8
from monitor.util.mysql_util import getconn,closeAll
from monitor import app

def get_popular_info(date,message):
    conn = getconn()
    cur = conn.cursor()
    id_list = message.keys()
    try:
        start_date = date.get('start_date')
        end_date = date.get('end_date')
        hxr_dic = {}
        for name_id in id_list:
            sql = "SELECT CAST(`create_data` AS CHAR),`popularity_score` FROM popularity WHERE '{}' <= `create_data`  AND `create_data` <= '{}' AND `candidate_id` ='{}' ORDER BY `create_data` ASC".format(start_date,end_date,name_id)
            # print(sql)
            re = cur.execute(sql)
            # print(count)
            if re < 1:
                return 'result','0'
            else:
                result = cur.fetchall()
                every_dic = {}
                for re in result:
                    every_dic[re[0]] = re[1]
                hxr_dic[message.get(name_id)] = every_dic
        return hxr_dic,'1'
    except Exception as erro:
        app.logger.error(erro)
        return str(erro),'2'
    finally:
        closeAll(conn,cur)


