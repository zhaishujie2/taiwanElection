from monitor.util.config import es_host, es_facebook_index, es_facebook_type, es_news_index, es_news_type, \
    es_twitter_index, es_twitter_type
from elasticsearch import Elasticsearch
from monitor.util.utilclass import get_date, get_time
import time

es = Elasticsearch(es_host, timeout=600)

def get_candidates(dict_name):
    try:
        date = time.strftime("%Y-%m-%d")
        print (date)
        start_time, end_time = get_time(date,date)
        sum = 0
        dict = {}
        face_dict = {}
        face_sum = 0
        for item in dict_name.keys():
            name = dict_name[item]
            query = {"query": {"bool": {"must": [{"term": {"keywords": name}},
                                                 {"range": {"timestamps": {"gt": start_time, "lt": end_time}}}]}},
                     "from": 0,
                     "size": 9999}
            result = es.search(index=es_news_index, doc_type=es_news_type, body=query)['hits']['hits']
            new_count = len(result)
            query = {"query": {"bool": {"must": [{"term": {"twitter_search": name}},
                                                 {"range": {"timestamps": {"gt": start_time, "lt": end_time}}}]}},
                     "from": 0,
                     "size": 9999}
            result = es.search(index=es_twitter_index, doc_type=es_twitter_type, body=query)['hits']['hits']
            print (query)
            twitter_count = len(result)
            print (twitter_count)
            name_count = twitter_count+new_count
            sum+=name_count
            dict[name] = name_count
            query = {"query": {"bool": {"must": [{"term": {"facebook_name": name}},
                                                 {"range": {"timestamps": {"gt": start_time, "lt": end_time}}}]}},
                     "from": 0,
                     "size": 9999}
            result = es.search(index=es_facebook_index, doc_type=es_facebook_type, body=query)['hits']['hits']
            facebook_count = 0
            for item in result:
                facebook_count+=int(item["_source"]["likes"])
            face_sum+=facebook_count
            face_dict[name] = facebook_count
        if sum ==0:
            pass
        else:
            flag = len(dict)
            duty = 1.0
            i=1
            for item in dict.keys():
                if i!=flag:
                    score = round(float(dict[item])/sum,3)
                    duty -= score
                    dict[item] = score
                else:
                    dict[item] = duty
        if face_sum ==0:
            pass
        else:
            flag = len(face_sum)
            duty = 1
            i=1
            for item in face_dict.keys():
                if i!=flag:
                    score = round(float(face_dict[item])/face_sum,3)
                    duty -= score
                    face_dict[item] = score
                else:
                    face_dict[item] = duty
        result_dict = {}
        result_dict["heat"] = dict
        result_dict["activity"] = face_dict
        return result_dict
    except Exception as e:
        return 0