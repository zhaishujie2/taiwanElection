# coding=utf-8
from monitor.util.mysql_util import getconn, closeAll
from monitor import app


# 获取地图的基本信息
def get_map_color(year):
    conn = getconn()
    cur = conn.cursor()
    try:
        sql = "select area.administrative_id,political.political from administrative_area as area,administrative_political  as political where area.administrative_id=political.administrative_id and political.`year`=%s"
        count = cur.execute(sql, year)
        result = cur.fetchmany(count)
        dict = {}
        if count == 0:
            app.logger.error("输入年份库中没有数据！当前输入的年份为：" + year)
            return 0
        for item in result:
            dict[item[0]] = item[1]
        return dict
    except (Exception) as e:
        app.logger.error(e)
        return 0
    finally:
        closeAll(conn, cur)


# 获取当前地区的选举人
def get_egional_electors(id, year):
    dict = {}
    conn = getconn()
    cur = conn.cursor()
    try:
        sql = "select candidate_id,username from candidate where  administrative_id=%s and `year`=%s"
        count = cur.execute(sql, (id, year))
        if count < 1:
            app.logger.error("当前省选举结果有问题，请与管理员联系前，输入的年份为：" + str(year) + "输入id:" + str(id))
            return dict
        result = cur.fetchmany(count)
        for item in result:
            dict[item[0]] = item[1]
        return dict
    except (Exception) as e:
        app.logger.error(e)
        return 0
    finally:
        closeAll(conn, cur)

# 获取当前地区的session
def get_session(id, year):
    dict_img = {}
    dict_partisan = {}
    conn = getconn()
    cur = conn.cursor()
    try:
        sql = "select candidate.candidate_id,candidate.username,partisan,image_name from candidate,candidate_personnel_information where  candidate_personnel_information.candidate_id=candidate.candidate_id and candidate.administrative_id=%s and candidate.`year`=%s"
        count = cur.execute(sql, (id, year))
        if count < 1:
            app.logger.error("当前省选举结果有问题，请与管理员联系前，输入的年份为：" + str(year) + "输入id:" + str(id))
            return 0
        result = cur.fetchmany(count)
        for item in result:
            dict_img[item[1]] = item[3]
            dict_partisan[item[1]] = item[2]
        return dict_img,dict_partisan
    except (Exception) as e:
        app.logger.error(e)
        return 0
    finally:
        closeAll(conn, cur)

# 获取当前选举人图片
def get_egional_images(id):
    conn = getconn()
    cur = conn.cursor()
    try:
        sql = "select image_name from candidate_personnel_information  where candidate_id =%s"
        cur.execute(sql, id)
        result = cur.fetchone()
        if result[0] == "":
            return 0
        return result[0]
    except (Exception) as e:
        return 0
    finally:
        closeAll(conn, cur)

