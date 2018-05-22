# coding=utf-8
import datetime
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
            sql = "select trend,date_time from google_trend where DATE(date_time) > %s and  DATE(date_time)< %s and candidate_id=%s"
            count = cur.execute(sql, (start_time, end_time, id))
            result = cur.fetchmany(count)
            dict_item = {}
            #Can be optimized
#---------------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------------
        return result
    except:
        return 0
    finally:
        closeAll(conn, cur)

def get_facebook_trend(start_time, end_time, dict_name):
    list_data = get_date(start_time, end_time)
    start_time, end_time = get_time(start_time, end_time)
    series_dict= {}
    table_list=[]
    upshot = {}
    for id, name in dict_name.items():
        link_dict = {}
        post_dict = {}
        for item in list_data:
            link_dict[item] = 0
            post_dict[item] = 0
        query = {"query": {"bool": {"must": [{"term": {"facebook_name": name}},
                                             {"range": {"timestamps": {"gt": start_time, "lt": end_time}}}]}},
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
            if post ==0 or link==0:
                aver_list.append(0)
            else:
                aver_list.append(int(link/post))
            sum_link+=link
            sum_post+=post
        series_dict[name] = aver_list
        dict = {}
        dict["name"] = name
        dict["total_likes"] = sum_link
        dict["total_post"] = sum_post
        dict["aver_likes"] = int(sum_link/sum_post)
        table_list.append(dict)
    upshot["echart"] = {"xAxis":list_data,"series":series_dict}
    upshot["table"] = table_list
    return upshot

