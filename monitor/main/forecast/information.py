# coding=utf-8
import datetime
from monitor.util.config import es_host,es_facebook_index,es_facebook_type,es_news_index,es_news_type,es_twitter_index,es_twitter_type
from elasticsearch import Elasticsearch
from monitor.util.utilclass import get_date, get_time,get_date_item
from monitor.util.mysql_util import getconn,closeAll
es = Elasticsearch(es_host, timeout=600)

def  get_google_trend(start_time,end_time,dict_name):
    conn = getconn()
    cur = conn.cursor()
    list_data = get_date(start_time,end_time)
    start_time = get_date_item(start_time)
    end_time = get_date_item(end_time)
    try:
        dict = {}
        for id in dict_name.keys():
            sql = "select trend,date_time from google_trend where DATE(date_time) > %s and  DATE(date_time)< %s and candidate_id=%s"
            count = cur.execute(sql,(start_time,end_time,id))
            result = cur.fetchmany(count)
            dict_item = {}
            for item  in result:
                dict_item [item[1].strftime("%Y-%m-%d")] = item[0]
            for item in list_data:
                if item not in dict_item:
                    dict_item[item] = 0
            dict[dict_name[id]] = dict_item
        result = {}
        result["xAxis"] = list_data
        result["series"] = dict
        return result
    except:
        return 0
    finally:
        closeAll(conn,cur)



if __name__ == '__main__':
    dict = {}
    dict["1"]="卢秀燕"
    dict["2"]="林佳龙"
    print (get_google_trend("2018-05-01","2018-05-07",dict))