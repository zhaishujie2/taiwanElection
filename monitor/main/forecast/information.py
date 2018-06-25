# coding=utf-8
import datetime
from monitor import app
from monitor.util.config import es_host, es_facebook_index, es_facebook_type, es_news_index, es_news_type, \
    es_twitter_index, es_twitter_type
from elasticsearch import Elasticsearch
from monitor.util.utilclass import get_date, get_time, get_date_item, get_timestamps_to_date
from monitor.util.mysql_util import getconn, closeAll

es = Elasticsearch(es_host, timeout=600)


def get_google_trend(start_time, end_time, dict_name):
    conn = getconn()
    cur = conn.cursor()
    list_data = get_date(start_time, end_time)
    start_time = get_date_item(start_time)
    end_time = get_date_item(end_time)
    series_dict = {}
    try:
        dict = {}
        for id in dict_name.keys():
            series = []
            sql = "select trend,date_time from google_trend where DATE(date_time) >= %s and  DATE(date_time)<= %s and candidate_id=%s"
            count = cur.execute(sql, (start_time, end_time, id))
            result = cur.fetchmany(count)
            dict_item = {}
            # Can be optimized
            # ---------------------------------------------------------------------------------------
            for item in result:
                dict_item[item[1].strftime("%Y-%m-%d")] = item[0]
            for item in list_data:
                if item not in dict_item:
                    dict_item[item] = 0
            dict[dict_name[id]] = dict_item
            for item in list_data:
                series.append(dict[dict_name[id]][item])
            series_dict[dict_name[id]] = series
        result = {}
        result["xAxis"] = list_data
        result["series"] = series_dict
        # -----------------------------------------------------------------------------------------
        return result
    except:
        return 0
    finally:
        closeAll(conn, cur)


def get_facebook_trend(start_time, end_time, dict_name):
    list_data = get_date(start_time, end_time)
    start_time, end_time = get_time(start_time, end_time)
    series_dict = {}
    table_list = []
    upshot = {}
    for id, name in dict_name.items():
        link_dict = {}
        post_dict = {}
        for item in list_data:
            link_dict[item] = 0
            post_dict[item] = 0
        query = {"query": {"bool": {"must": [{"term": {"facebook_name": name}},
                                             {"range": {"timestamps": {"gte": start_time, "lte": end_time}}}]}},
                 "from": 0,
                 "size": 9999}
        result = es.search(index=es_facebook_index, doc_type=es_facebook_type, body=query)['hits']['hits']
        for item in result:
            date = get_timestamps_to_date(item["_source"]["timestamps"])
            post_dict[date] = post_dict[date] + 1
            link_dict[date] = link_dict[date] + int(item["_source"]["likes"])
        aver_list = []
        sum_post = 0
        sum_link = 0
        for item in list_data:
            post = int(post_dict[item])
            link = int(link_dict[item])
            if post == 0 or link == 0:
                aver_list.append(0)
            else:
                aver_list.append(int(link / post))
            sum_link += link
            sum_post += post
        series_dict[name] = aver_list
        dict = {}
        dict["name"] = name
        dict["total_likes"] = sum_link
        dict["total_post"] = sum_post
        dict["aver_likes"] = int(sum_link / sum_post)
        table_list.append(dict)
    upshot["echart"] = {"xAxis": list_data, "series": series_dict}
    upshot["table"] = table_list
    return upshot


# 获取支持率
def get_popular_info(start_time, end_time, message):
    conn = getconn()
    cur = conn.cursor()
    id_list = message.keys()
    list_data = get_date(start_time, end_time)
    try:
        hxr_dic = {}
        series_dict = {}
        for name_id in id_list:
            sql = """SELECT CAST(`create_data` AS CHAR),`popularity_score`,`candidate_id` FROM popularity WHERE %s <= `create_data`  AND `create_data` <= %s AND `candidate_id` = %s ORDER BY `create_data` ASC"""
            re = cur.execute(sql, (start_time, end_time, name_id))
            if re < 1:
                return 0
            else:
                result = cur.fetchall()
                every_dic = {}
                for re in result:
                    every_dic[re[0]] = re[1]
                # hxr_dic[message.get(name_id)] = every_dic
                for date in list_data:
                    if date not in every_dic:
                        every_dic[date] = 0
                hxr_dic[message.get(name_id)] = every_dic
                series = []
                for item in list_data:
                    series.append(hxr_dic[message.get(name_id)][item])
                series_dict[message.get(name_id)] = series
        result = {}
        result["xAxis"] = list_data
        result["series"] = series_dict
        return result
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 获取当前月份的民调数据
def get_current_support_info(year, dict_name):
    conn = getconn()
    cur = conn.cursor()
    try:
        result = []
        for id, name in dict_name.items():
            year = str(year) + "%"
            item_dict = {}
            sql = "SELECT * FROM poll_support WHERE candidate_id=%s and support_time LIKE %s ORDER BY support_time DESC"
            count = cur.execute(sql, (id, year))
            if count == 0:
                item_dict["name"] = name
                item_dict["20s-30s"] = 0
                item_dict["30s-40s"] = 0
                item_dict["40s-50s"] = 0
                item_dict["50s-60s"] = 0
                item_dict["60s-70s"] = 0
                item_dict["70s"] = 0
                item_dict["network_support"] = 0
                item_dict["total_support"] = 0
            else:
                item = cur.fetchone()
                item_dict["name"] = name
                item_dict["20s-30s"] = item[2]
                item_dict["30s-40s"] = item[3]
                item_dict["40s-50s"] = item[4]
                item_dict["50s-60s"] = item[5]
                item_dict["60s-70s"] = item[6]
                item_dict["70s"] = item[7]
                item_dict["network_support"] = item[8]
                item_dict["total_support"] = item[9]
            result.append(item_dict)
        return result
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 获取当前年的民调数据汇总
def get_year_support_info(year, dict_name):
    conn = getconn()
    cur = conn.cursor()
    try:
        year = str(year) + "%"
        where_name = ""
        for id, name in dict_name.items():
            where_name += ("candidate_id=" + str(id) + " or ")
        where_name = where_name[:-3]
        sql = "SELECT support_time FROM poll_support WHERE " + where_name + "and support_time LIKE %s  group by support_time ORDER BY support_time ASC "
        xAxis_count = cur.execute(sql, year)
        xAxis_data = cur.fetchmany(xAxis_count)
        xAxis_dict = {}
        xAxis = []
        series = []
        xAxis_flag = 0
        for item in xAxis_data:
            xAxis_dict[item[0]] = xAxis_flag
            xAxis.append(str(int(item[0].split("-")[1])) + "月")
            xAxis_flag += 1
        for id, name in dict_name.items():
            item_list = []
            sql = "SELECT total_support,support_time FROM poll_support WHERE candidate_id=%s and support_time LIKE %s ORDER BY support_time ASC"
            item_count = cur.execute(sql, (id, year))
            item_data = cur.fetchmany(item_count)
            if item_count == xAxis_count:
                for item in item_data:
                    item_list.append(item[0])
            else:
                for i in range(0, xAxis_count):
                    item_list.append(0)
                for item in item_data:
                    item_list[xAxis_dict[item[1]]] = item[0]
            series.append({name: item_list})
        return {"xAxis": xAxis, "series": series}
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


# 获取流量数据汇总
def get_flow_info(dict_name):
    dict = {}
    conn = getconn()
    cur = conn.cursor()
    try:
        pv_today_count = 0
        pv_7day_count = 0
        pv_30day_count = 0
        uv_today_count = 0
        uv_7day_count = 0
        uv_30day_count = 0
        pv_today = 1
        pv_7day = 1
        pv_30day = 1
        uv_today = 1
        uv_7day = 1
        uv_30day = 1
        for id, name in dict_name.items():
            item_dict = {}
            sql = "SELECT * FROM flow WHERE candidate_id=%s ORDER BY `time` DESC LIMIT 1"
            print(sql, id)
            item_count = cur.execute(sql, id)
            if item_count != 0:
                item_data = cur.fetchone()
                item_dict["pv_today"] = item_data[2]
                item_dict["pv_7day"] = item_data[3]
                item_dict["pv_30day"] = item_data[4]
                item_dict["uv_today"] = item_data[6]
                item_dict["uv_7day"] = item_data[7]
                item_dict["uv_30day"] = item_data[8]
                pv_today_count += int(item_data[2])
                pv_7day_count += int(item_data[3])
                pv_30day_count += int(item_data[4])
                uv_today_count += int(item_data[6])
                uv_7day_count += int(item_data[7])
                uv_30day_count += int(item_data[8])
                dict[name] = item_dict
            else:
                item_data = cur.fetchone()
                item_dict["pv_today"] = 0
                item_dict["pv_7day"] = 0
                item_dict["pv_30day"] = 0
                item_dict["uv_today"] = 0
                item_dict["uv_7day"] = 0
                item_dict["uv_30day"] = 0
                dict[name] = item_dict
        count = len(dict)
        flag = 1
        for name, item in dict.items():
            if flag != count:
                if pv_today_count == 0:
                    dict[name]["pv_today"] = 0
                else:
                    dict[name]["pv_today"] = round(int(item["pv_today"]) / pv_today_count, 2)
                    pv_today -= round(int(item["pv_today"]) / pv_today_count, 2)
                if pv_7day_count == 0:
                    dict[name]["pv_7day"] = 0
                else:
                    dict[name]["pv_7day"] = round(int(item["pv_7day"]) / pv_7day_count, 2)
                    pv_7day -= round(int(item["pv_7day"]) / pv_7day_count, 2)

                if pv_30day_count == 0:
                    dict[name]["pv_30day"] = 0
                else:
                    dict[name]["pv_30day"] = round(int(item["pv_30day"]) / pv_30day_count, 2)
                    pv_30day -= round(int(item["pv_30day"]) / pv_30day_count, 2)
                if uv_today_count == 0:
                    dict[name]["uv_today"] = 0
                else:
                    dict[name]["uv_today"] = round(int(item["uv_today"]) / uv_today_count, 2)
                    uv_today -= round(int(item["uv_today"]) / uv_today_count, 2)
                if uv_7day_count == 0:
                    dict[name]["uv_7day"] = 0
                else:
                    dict[name]["uv_7day"] = round(int(item["uv_7day"]) / uv_7day_count, 2)
                    uv_7day -= round(int(item["uv_7day"]) / uv_7day_count, 2)
                if uv_30day_count == 0:
                    dict[name]["uv_today"] = 0
                else:
                    dict[name]["uv_30day"] = round(int(item["uv_30day"]) / uv_30day_count, 2)
                    uv_30day -= round(int(item["uv_30day"]) / uv_30day_count, 2)
                count += 1
            else:
                dict[name]["pv_today"] = round(pv_today, 2)
                dict[name]["pv_7day"] = round(pv_7day, 2)
                dict[name]["pv_30day"] = round(pv_30day, 2)
                dict[name]["uv_today"] = round(uv_today, 2)
                dict[name]["uv_7day"] = round(uv_7day, 2)
                dict[name]["uv_30day"] = round(uv_30day, 2)
        return dict
    except Exception as erro:
        app.logger.error(erro)
        return 0
    finally:
        closeAll(conn, cur)


if __name__ == '__main__':
    dict = {}
    dict[1] = "卢秀燕"
    dict[2] = "林佳龙"
    result = get_flow_info(dict)
    print(result)
