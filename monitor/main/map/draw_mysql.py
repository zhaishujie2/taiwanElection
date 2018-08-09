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
        return dict_img, dict_partisan
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


def get_partisan(id):
    conn = getconn()
    cur = conn.cursor()
    try:
        sql = "select partisan from candidate_personnel_information  where candidate_id =%s"
        cur.execute(sql, id)
        result = cur.fetchone()
        if result[0] == "":
            return "无党"
        if result[0] == None:
            return "无党"
        return result[0]
    except (Exception) as e:
        return "无党"
    finally:
        closeAll(conn, cur)


def get_popularity_partisan(year):
    conn = getconn()
    cur = conn.cursor()
    dict = {}
    try:
        sql = "select m.a as area ,partisan from popularity,(select max(popularity_score) as s ,m.s as t ,m.n as a from  popularity ,(select max(create_data) as s,administrative_id as n  from popularity where `year`=%s GROUP BY administrative_id )m where administrative_id = m.n  and create_data=m.s GROUP BY administrative_id)m ,candidate_personnel_information where create_data = m.t and administrative_id = m.a and popularity_score = m.s and popularity.candidate_id = candidate_personnel_information.candidate_id"
        count = cur.execute(sql, year)
        if count == 0:
            return 0
        else:
            result = cur.fetchmany(count)
            for item in result:
                dict[item[0]] = item[1]
            return dict
        return 0
    except (Exception) as e:
        return 0
    finally:
        closeAll(conn, cur)


def get_popularity_partisan_compared(year):
    cnp = 0
    dpp = 0
    other = 0
    result = get_popularity_partisan(year)
    for k, v in result.items():
        if v == "国民党":
            cnp += 1
        elif v == "民进党":
            dpp += 1
        else:
            other += 1
    return {"cnp": cnp, "dpp": dpp, "other": other}


def partisan_compared(year):
    present = get_map_color(year)
    popularity = get_popularity_partisan(year)
    dpp = []
    cnp = []
    other = []
    unchang_dpp = []
    unchang_cnp = []
    unchang_other = []
    for key in present.keys():
        if (present[key] == popularity[key]):
            if (present[key] =="国民党"):
                unchang_cnp.append(key)
            elif (present[key] =="民进党"):
                unchang_dpp.append(key)
            else:
                unchang_other.append(key)
        else:
            #         if present[key] == "国民党" and popularity[key] == "民进党":
            #             cnp_dpp.append(key)
            #         elif present[key] == "民进党" and popularity[key] == "国民党":
            #             dpp_cnp.append(key)
            #         elif present[key] == "国民党" and popularity[key] != "民进党":
            #             cnp_other.append(key)
            #         elif present[key] == "民进党" and popularity[key] != "国民党":
            #             dpp_other.append(key)
            #         elif present[key]!="国民党" and present[key]!="民进党" and popularity[key] == "国民党":
            #             other_cnp.append(key)
            #         elif present[key]!="国民党" and present[key]!="民进党" and popularity[key] == "民进党":
            #             other_dpp.append(key)
            # return {"cnp_dpp":cnp_dpp,"dpp_cnp":dpp_cnp,"cnp_other":cnp_other,"dpp_other":dpp_other,"other_cnp":other_cnp,"other_dpp":other_dpp}
            if (popularity[key]) == "民进党":
                dpp.append(key)
            elif (popularity[key]) == "国民党":
                cnp.append(key)
            else:
                other.append(key)
    return {"change": {"cnp": cnp, "dpp": dpp, "other": other}, "unchange": {"cnp":unchang_cnp,"dpp":unchang_dpp,"other":unchang_other}}


