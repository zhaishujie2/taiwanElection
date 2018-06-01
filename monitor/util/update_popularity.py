# coding=utf-8
import sys

sys.path.append('/data/taiwan/taiwanElection')
from monitor.util.config import fb_weight, tw_weight, news_weight, ptt_weight, es_host, es_facebook_index, \
    es_facebook_type, es_news_index, es_news_type, es_twitter_index, es_twitter_type, es_forum_type, es_forum_index, \
    year
from monitor.util.utilclass import get_time, get_before_time, get_date
from monitor.util.mysql_util import getconn, closeAll
from elasticsearch import Elasticsearch
import datetime

es = Elasticsearch(es_host, timeout=600)


def update_popularity_demo(start_time, end_time):
    conn = getconn()
    cur = conn.cursor()
    try:
        sql = "SELECT administrative_id from candidate where `year`=%s GROUP BY administrative_id"
        count = cur.execute(sql, year)
        result = cur.fetchmany(count)
        for item in result:
            sql = "SELECT * from candidate where administrative_id=%s and `year`=%s"
            count = cur.execute(sql, (item[0], year))
            data = cur.fetchmany(count)
            dict = {}
            for person in data:
                dict[person[0]] = person[2]
            popularity_dict = (get_popularity(start_time, end_time, dict))
            for key, value in dict.items():
                sql = "UPDATE popularity SET popularity_score=%s WHERE candidate_id=%s AND create_data=%s"
                print(popularity_dict[value] * 100)
                cur.execute(sql, (popularity_dict[value] * 100, key, end_time))
                conn.commit()
    except:
        return 0
    finally:
        closeAll(conn, cur)


def get_popularity(start_time, end_time, dict_name):
    try:
        start_time, end_time = get_time(start_time, end_time)
        fb = get_fb_aver_link(dict_name, start_time, end_time)
        tw = get_tw_count(dict_name, start_time, end_time)
        news = get_news_count(dict_name, start_time, end_time)
        ptt = get_ptt_popularity(dict_name, start_time, end_time)
        count = 1
        dict = {}
        flat = 1
        for id in dict_name.keys():
            if count == len(dict_name):
                dict[dict_name[id]] = round(flat, 3)
            else:
                sorce = round((fb[dict_name[id]] * fb_weight + ptt[dict_name[id]] * ptt_weight + tw[
                    dict_name[id]] * tw_weight + news[dict_name[id]] * news_weight), 3)
                dict[dict_name[id]] = sorce
                flat -= sorce
        return dict
    except:
        return 0


def get_fb_aver_link(dict_name, start_time, end_time):
    try:
        sum = 0
        dict = {}
        for id in dict_name.keys():
            likes = 0
            name = dict_name[id]
            query = {"query": {"bool": {"must": [{"term": {"facebook_name": name}},
                                                 {"range": {"timestamps": {"gt": start_time, "lt": end_time}}}]}},
                     "from": 0,
                     "size": 10000}
            result = es.search(index=es_facebook_index, doc_type=es_facebook_type, body=query)['hits']['hits']
            for item in result:
                if int(item["_source"]["likes"]) > 4000:
                    pass
                else:
                    likes += int(item["_source"]["likes"])
            dict[dict_name[id]] = int(likes / (len(result)))
            sum += int(likes / (len(result)))
        print
        count = 1
        flat = 1
        result_dict = {}
        if sum == 0:
            for item in dict.keys():
                if count == len(dict):
                    result_dict[item] = round(flat, 3)
                else:
                    result_dict[item] = round(1 / len(dict), 3)
                    flat -= round(1 / len(dict), 3)
                    count += 1
        else:
            for item in dict.keys():
                if count == len(dict):
                    result_dict[item] = flat
                else:
                    result_dict[item] = round(float(dict[item]) / sum, 3)
                    flat -= round(float(dict[item]) / sum, 3)
                    count += 1
        return result_dict
    except:
        return 0


def get_tw_count(dict_name, start_time, end_time):
    try:
        sum = 0
        dict = {}
        for id in dict_name.keys():
            name = dict_name[id]
            query = {"query": {"bool": {"must": [{"term": {"twitter_search": name}},
                                                 {"range": {"timestamps": {"gt": start_time, "lt": end_time}}}]}},
                     "from": 0,
                     "size": 10000}
            result = es.search(index=es_twitter_index, doc_type=es_twitter_type, body=query)['hits']['hits']
            dict[name] = len(result)
            sum += len(result)
        count = 1
        flat = 1
        result_dict = {}
        if sum == 0:
            for item in dict.keys():
                if count == len(dict):
                    result_dict[item] = flat
                else:
                    result_dict[item] = round(1 / len(dict), 3)
                    flat -= round(1 / len(dict), 3)
                    count += 1
        else:
            for item in dict.keys():
                if count == len(dict):
                    result_dict[item] = round(flat, 3)
                else:
                    result_dict[item] = round(float(dict[item]) / sum, 3)
                    flat -= round(float(dict[item]) / sum, 3)
                    count += 1
        return result_dict
    except:
        return 0


def get_news_count(dict_name, start_time, end_time):
    try:
        sum = 0
        dict = {}
        for id in dict_name.keys():
            name = dict_name[id]
            query = {"query": {"bool": {"must": [{"term": {"keywords": name}},
                                                 {"range": {"timestamps": {"gt": start_time, "lt": end_time}}}]}},
                     "from": 0,
                     "size": 10000}
            result = es.search(index=es_news_index, doc_type=es_news_type, body=query)['hits']['hits']
            dict[name] = len(result)
            sum += len(result)
        count = 1
        flat = 1
        result_dict = {}
        if sum == 0:
            for item in dict.keys():
                if count == len(dict):
                    result_dict[item] = flat
                else:
                    result_dict[item] = round(1 / len(dict), 3)
                    flat -= round(1 / len(dict), 3)
                    count += 1
        else:
            for item in dict.keys():
                if count == len(dict):
                    result_dict[item] = flat
                else:
                    result_dict[item] = round(float(dict[item]) / sum, 3)
                    flat -= round(float(dict[item]) / sum, 3)
                    count += 1
        return result_dict
    except:
        return 0


def get_ptt_popularity(dict_name, start_time, end_time):
    try:
        sum = 0
        dict = {}
        for id in dict_name.keys():
            likes = 0
            name = dict_name[id]
            query = {"query": {"bool": {"must": [{"term": {"keywords": name}},
                                                 {"range": {"timestamps": {"gt": start_time, "lt": end_time}}}]}},
                     "from": 0,
                     "size": 10000}
            result = es.search(index=es_forum_index, doc_type=es_forum_type, body=query)['hits']['hits']
            for item in result:
                likes += int(item["_source"]["likes"])
                likes -= int(item["_source"]["tread"])
            dict[dict_name[id]] = likes
            sum += likes
        count = 1
        flat = 1
        result_dict = {}
        if sum == 0:
            for item in dict.keys():
                if count == len(dict):
                    result_dict[item] = flat
                else:
                    result_dict[item] = round(1 / len(dict), 3)
                    flat -= round(1 / len(dict), 3)
                    count += 1
        else:
            for item in dict.keys():
                if count == len(dict):
                    result_dict[item] = flat
                else:
                    result_dict[item] = round(float(dict[item]) / sum, 3)
                    flat -= round(float(dict[item]) / sum, 3)
                    count += 1
        return result_dict
    except:
        return 0


if __name__ == '__main__':
    # end_time = datetime.datetime.now().strftime("%Y-%m-%d")
    # list = get_date("2018-2-15",end_time)
    # for item in list:
    #     start_time = get_before_time(item,45)
    #     insert_popularity_demo(start_time,item)
    end_time = datetime.datetime.now().strftime("%Y-%m-%d")
    start_time = get_before_time(end_time, 45)
    print(update_popularity_demo(start_time, end_time))
