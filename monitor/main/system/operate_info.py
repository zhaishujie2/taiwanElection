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
        insert_sql = """INSERT INTO spider_infos (`administrative_id`,administrative_name,`year`,facebook_url) VALUES ('{}','{}','{}','{}')""".format(administrative_id,administrative_name,year,facebook_url)
        # print(insert_sql)
        re = cur.execute(insert_sql)
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
    print(ids)
    try:
        delete_sql = """DELETE FROM `spider_infos` WHERE id = '{}'""".format(ids)
        re = cur.execute(delete_sql)
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

        select_sql = """SELECT * FROM `spider_infoss` WHERE  """ + where_sql
        # print(select_sql)
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
            return lists
    except Exception as erro:
        app.logger.error(erro)
        return str(erro)
    finally:
        closeAll(conn,cur)


# if __name__ == '__main__':
#     # a = insert_info('7017','李晨','2018','www.facebook.com')
#     a = delete_info(11)#{"administrative_id":"7019","administrative_name":"李晨"}
#     # a = select_info({"administrative_id":"7017","administrative_name":"李晨","year":"2018","facebook_url":"www.baidu.com"})
#     # a = update_info(up_dict={"administrative_id":"7020","administrative_name":"lichen"},where_dict={"administrative_id":"7019","administrative_name":"李晨"})
#     # a = select_info({"administrative_name":"李晨","year":"2020"})
#     print(a)


