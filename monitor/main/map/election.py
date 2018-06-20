# coding=utf-8

from monitor.util.config import fb_weight, tw_weight, news_weight, ptt_weight, es_host, es_facebook_index, \
    es_facebook_type, es_news_index, es_news_type, es_twitter_index, es_twitter_type, es_forum_type, es_forum_index
from monitor.util.utilclass import get_time
from elasticsearch import Elasticsearch

es = Elasticsearch(es_host, timeout=600)


def get_popularity(start_time, end_time, dict_name):
    try:
        start_time, end_time = get_time(start_time, end_time)
        fb = get_fb_aver_link(dict_name, start_time, end_time)
        tw = get_tw_count(dict_name, start_time, end_time)
        news = get_news_count(dict_name, start_time, end_time)
        ptt = get_ptt_popularity(dict_name, start_time, end_time)
        if fb ==0:
            fb = {}
            for key,value in dict_name.items():
                fb[value] = 0
        if tw ==0:
            tw = {}
            for key,value in dict_name.items():
                tw[value] = 0
        if news ==0:
            news = {}
            for key,value in dict_name.items():
                news[value] = 0
        if ptt ==0:
            ptt = {}
            for key,value in dict_name.items():
                ptt[value] = 0
        count = 1
        dict = {}
        flat = 1
        sum = 0
        result_dict={}
        for id in dict_name.keys():
            sorce = round((fb[dict_name[id]] * fb_weight + ptt[dict_name[id]] * ptt_weight + tw[
                dict_name[id]] * tw_weight + news[dict_name[id]] * news_weight), 3)
            dict[dict_name[id]] = sorce
            sum+=sorce
        for id in dict_name.keys():
            if count == len(dict_name):
                result_dict[dict_name[id]] = round(flat, 3)
            else:
                sorce = dict[dict_name[id]] / sum
                result_dict[dict_name[id]] = sorce
                flat -= sorce
                print (flat)
                count +=1
        return result_dict
    except :
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
                if likes <=0:
                    likes = 0
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
    dict_name={}
    dict_name[23] = "陈学圣"
    dict_name[69] = "郑文灿"
    data = get_popularity("2018-05-05","2018-06-20",dict_name)
    print (data)