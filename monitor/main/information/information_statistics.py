# coding=utf-8
import datetime
from monitor.util.config import es_host,es_facebook_index,es_facebook_type,es_news_index,es_news_type,es_twitter_index,es_twitter_type
from elasticsearch import Elasticsearch
from monitor.util.utilclass import get_date, get_time

es = Elasticsearch(es_host, timeout=600)

def get_information_facebook_statistics_count(start_time, end_time,dict_name):
    start_timestamps, end_timestamps = get_time(start_time, end_time)
    data_list = get_date(start_time, end_time)
    if start_timestamps==0 or end_timestamps == 0 or dict_name == 0:
        return None
    statistics = {}
    dict = {}
    for item in dict_name.keys():
        data_dict = {}
        count_list = []
        name = dict_name[item]
        query = {"query": {"bool": {"must": [{"range": {"timestamps": {"gt": start_timestamps, "lt": end_timestamps}}},
                                         {"term": {"facebook_name": name}}], "must_not": [], "should": []}}, "from": 0,
             "size": 10000, "sort": [], "aggs": {}}
        result = es.search(index=es_facebook_index, doc_type=es_facebook_type, body=query)['hits']['hits']
        for item in data_list:
            data_dict[item]=0
        for item in result:
            item_data= item["_source"]["time"].split(" ")[0]
            data_dict[item_data] = data_dict[item_data]+1
        for key in data_dict.keys():
            count_list.append(data_dict[key])
        dict[name] = count_list
    statistics["person"] = dict
    statistics["date"] = data_list
    return statistics

def get_information_news_statistics_count(start_time, end_time,dict_name):
    start_timestamps, end_timestamps = get_time(start_time, end_time)
    data_list = get_date(start_time, end_time)
    if start_timestamps==0 or end_timestamps == 0 or dict_name == 0:
        return None
    statistics = {}
    dict = {}
    for item in dict_name.keys():
        count_list = []
        data_dict = {}
        name = dict_name[item]
        query = {"query": {"bool": {"must": [{"range": {"timestamps": {"gt": start_timestamps, "lt": end_timestamps}}},
                                             {"term": {"keywords": name}}], "must_not": [], "should": []}}, "from": 0,
                 "size": 10000, "sort": [], "aggs": {}}
        result = es.search(index=es_news_index, doc_type=es_news_type, body=query)['hits']['hits']
        for item in data_list:
            data_dict[item]=0
        for item in result:
            item_data= item["_source"]["time"].split(" ")[0]
            data_dict[item_data] = data_dict[item_data]+1
        for key in data_dict.keys():
            count_list.append(data_dict[key])
        dict[name] = count_list
    statistics["person"] = dict
    statistics["date"] = data_list
    return statistics


def get_information_twitter_statistics_count(start_time, end_time,dict_name):
    start_timestamps, end_timestamps = get_time(start_time, end_time)
    data_list = get_date(start_time, end_time)
    if start_timestamps==0 or end_timestamps == 0 or dict_name == 0:
        return None
    statistics = {}
    dict = {}
    for item in dict_name.keys():
        count_list = []
        data_dict = {}
        name = dict_name[item]
        query = {"query": {"bool": {"must": [{"range": {"timestamps": {"gt": start_timestamps, "lt": end_timestamps}}},
                                             {"term": {"twitter_search": name}}], "must_not": [], "should": []}}, "from": 0,
                 "size": 10000, "sort": [], "aggs": {}}
        result = es.search(index=es_twitter_index, doc_type=es_twitter_type, body=query)['hits']['hits']
        for item in data_list:
            data_dict[item]=0
        for item in result:
            item_data= item["_source"]["time"].split(" ")[0]
            data_dict[item_data] = data_dict[item_data]+1
        for key in data_dict.keys():
            count_list.append(data_dict[key])
        dict[name] = count_list
    statistics["person"] = dict
    statistics["date"] = data_list
    return statistics

#获取facebook 某时间段某个人的数据
def get_facebook_pages(name,start_date,end_date):
    start_timestamps, end_timestamps = get_time(start_date,end_date)
    if start_timestamps==0 or end_timestamps == 0 :
        return None
    query = {"query": {"bool": {"must": [{"range": {"timestamps": {"gt": start_timestamps, "lt": end_timestamps}}},
                                         {"term": {"facebook_name": name}}], "must_not": [], "should": []}}, "from": 0,
             "size": 10000, "sort": [], "aggs": {}}
    result = es.search(index=es_facebook_index, doc_type=es_facebook_type, body=query)['hits']['hits']
    return len(result)

def get_facebook_data(name,page_number,page_size,start_date,end_date):
    start_from = (page_number-1)*page_size
    start_timestamps, end_timestamps = get_time(start_date, end_date)
    if start_timestamps==0 or end_timestamps == 0 :
        return None
    query = {"query": {"bool": {"must": [{"range": {"timestamps": {"gt": start_timestamps, "lt": end_timestamps}}},
                                         {"term": {"facebook_name": name}}], "must_not": [], "should": []}}, "from": start_from,
             "size": page_size, "sort": [], "aggs": {}}
    result = es.search(index=es_facebook_index, doc_type=es_facebook_type, body=query)['hits']['hits']
    list = []
    for item in result:
        dict = {}
        dict["context"] = item["_source"]["context"]
        dict["likes"] = item["_source"]["likes"]
        dict["facebook_name"] = item["_source"]["facebook_name"]
        dict["comment"] = item["_source"]["comment"]
        dict["time"] = item["_source"]["time"].split(" ")[0]
        list.append(dict)
    return list


#获取facebook某时间段所有的数据
def get_all_facebook_pages(dict_name,start_date,end_date):
    start_timestamps, end_timestamps = get_time(start_date, end_date)
    if start_timestamps==0 or end_timestamps == 0 :
        return None
    list = []
    for item in dict_name.keys():
        dict = {}
        dict["term"] = {"facebook_name":dict_name[item]}
        list.append(dict)
    query = {"query": {"bool": {"must": [{"range": {"timestamps": {"gt": start_timestamps, "lt": end_timestamps}}}], "must_not": [], "should": list}}, "from": 0,
                 "size": 10000, "sort": [], "aggs": {}}
    result = es.search(index=es_facebook_index, doc_type=es_facebook_type, body=query)['hits']['hits']
    return (len(result))


def get_all_facebook_data(dict_name,page_number,page_size,start_date,end_date):
    start_from = (page_number-1)*page_size
    start_timestamps, end_timestamps = get_time(start_date, end_date)
    if start_timestamps==0 or end_timestamps == 0 :
        return None
    list = []
    for item in dict_name.keys():
        dict = {}
        dict["term"] = {"facebook_name":dict_name[item]}
        list.append(dict)
    query = {"query": {"bool": {"must": [{"range": {"timestamps": {"gt": start_timestamps, "lt": end_timestamps}}}], "must_not": [], "should": list}}, "from": start_from,
             "size": page_size, "sort": [], "aggs": {}}
    result = es.search(index=es_facebook_index, doc_type=es_facebook_type, body=query)['hits']['hits']
    list = []
    for item in result:
        dict = {}
        dict["context"] = item["_source"]["context"]
        dict["likes"] = item["_source"]["likes"]
        dict["facebook_name"] = item["_source"]["facebook_name"]
        dict["comment"] = item["_source"]["comment"]
        dict["time"] = item["_source"]["time"].split(" ")[0]
        list.append(dict)
    return list

#获取news 某时间段天某个人的数据
def get_news_pages(name,start_date,end_date):
    start_timestamps, end_timestamps = get_time(start_date,end_date)
    if start_timestamps==0 or end_timestamps == 0 :
        return None
    query = {"query": {"bool": {"must": [{"range": {"timestamps": {"gt": start_timestamps, "lt": end_timestamps}}},
                                         {"term": {"keywords": name}}], "must_not": [], "should": []}}, "from": 0,
             "size": 10000, "sort": [], "aggs": {}}
    result = es.search(index=es_news_index, doc_type=es_news_type, body=query)['hits']['hits']
    return len(result)

def get_news_data(name,page_number,page_size,start_date,end_date):
    start_from = (page_number-1)*page_size
    start_timestamps, end_timestamps = get_time(start_date, end_date)
    if start_timestamps==0 or end_timestamps == 0 :
        return None
    query = {"query": {"bool": {"must": [{"range": {"timestamps": {"gt": start_timestamps, "lt": end_timestamps}}},
                                         {"term": {"keywords": name}}], "must_not": [], "should": []}}, "from": start_from,
             "size": page_size, "sort": [], "aggs": {}}
    result = es.search(index=es_news_index, doc_type=es_news_type, body=query)['hits']['hits']
    list = []
    for item in result:
        dict = {}
        dict["context"] = item["_source"]["context"]
        dict["source"] = item["_source"]["news_source"]
        dict["keywords"] = item["_source"]["keywords"]
        dict["title"] = item["_source"]["title"]
        dict["summary"] = item["_source"]["summary"]
        dict["url"] = item["_source"]["url"]
        dict["images"] = item["_source"]["images"]
        dict["time"] = item["_source"]["time"].split(" ")[0]
        list.append(dict)
    return list


#获取news当天所有的数据
def get_all_news_pages(dict_name,start_date,end_date):
    start_timestamps, end_timestamps = get_time(start_date, end_date)
    if start_timestamps==0 or end_timestamps == 0 :
        return None
    list = []
    for item in dict_name.keys():
        dict = {}
        dict["term"] = {"keywords":dict_name[item]}
        list.append(dict)
    query = {"query": {"bool": {"must": [{"range": {"timestamps": {"gt": start_timestamps, "lt": end_timestamps}}}], "must_not": [], "should": list}}, "from": 0,
             "size": 10000, "sort": [], "aggs": {}}
    result = es.search(index=es_news_index, doc_type=es_news_type, body=query)['hits']['hits']
    return (len(result))


def get_all_news_data(dict_name,page_number,page_size,start_date,end_date):
    start_from = (page_number-1)*page_size
    start_timestamps, end_timestamps = get_time(start_date, end_date)
    if start_timestamps==0 or end_timestamps == 0 :
        return None
    list = []
    for item in dict_name.keys():
        dict = {}
        dict["term"] = {"keywords":dict_name[item]}
        list.append(dict)
    query = {"query": {"bool": {"must": [{"range": {"timestamps": {"gt": start_timestamps, "lt": end_timestamps}}}], "must_not": [], "should": list}}, "from": start_from,
             "size": page_size, "sort": [], "aggs": {}}
    result = es.search(index=es_news_index, doc_type=es_news_type, body=query)['hits']['hits']
    list = []
    for item in result:
        dict = {}
        dict["context"] = item["_source"]["context"]
        dict["source"] = item["_source"]["news_source"]
        dict["keywords"] = item["_source"]["keywords"]
        dict["title"] = item["_source"]["title"]
        dict["summary"] = item["_source"]["summary"]
        dict["url"] = item["_source"]["url"]
        dict["images"] = item["_source"]["images"]
        dict["time"] = item["_source"]["time"].split(" ")[0]
        list.append(dict)
    return list





#获取twitter 某时间段天某个人的数据
def get_twitter_pages(name,start_date,end_date):
    start_timestamps, end_timestamps = get_time(start_date,end_date)
    if start_timestamps==0 or end_timestamps == 0 :
        return None
    query = {"query": {"bool": {"must": [{"range": {"timestamps": {"gt": start_timestamps, "lt": end_timestamps}}},
                                         {"term": {"twitter_search": name}}], "must_not": [], "should": []}}, "from": 0,
             "size": 10000, "sort": [], "aggs": {}}
    result = es.search(index=es_twitter_index, doc_type=es_twitter_type, body=query)['hits']['hits']
    return len(result)

def get_twitter_data(name,page_number,page_size,start_date,end_date):
    start_from = (page_number-1)*page_size
    start_timestamps, end_timestamps = get_time(start_date, end_date)
    query = {"query": {"bool": {"must": [{"range": {"timestamps": {"gt": start_timestamps, "lt": end_timestamps}}},
                                         {"term": {"twitter_search": name}}], "must_not": [], "should": []}}, "from": start_from,
             "size": page_size, "sort": [], "aggs": {}}
    result = es.search(index=es_twitter_index, doc_type=es_twitter_type, body=query)['hits']['hits']
    list = []
    for item in result:
        dict = {}
        dict["context"] = item["_source"]["context"]
        dict["likes"] = item["_source"]["likes"]
        dict["name"] = item["_source"]["twitter_search"]
        dict["twitter_name"] = item["_source"]["twitter_name"]
        dict["comment"] = item["_source"]["comment"]
        dict["time"] = item["_source"]["time"].split(" ")[0]
        list.append(dict)
    return list


#获取twitter当天所有的数据
def get_all_twitter_pages(dict_name,start_date,end_date):
    start_timestamps, end_timestamps = get_time(start_date, end_date)
    if start_timestamps==0 or end_timestamps == 0 :
        return None
    list = []
    for item in dict_name.keys():
        dict = {}
        dict["term"] = {"twitter_search":dict_name[item]}
        list.append(dict)
    query = {"query": {"bool": {"must": [{"range": {"timestamps": {"gt": start_timestamps, "lt": end_timestamps}}}], "must_not": [], "should": list}}, "from": 0,
             "size": 10000, "sort": [], "aggs": {}}
    result = es.search(index=es_twitter_index, doc_type=es_twitter_type, body=query)['hits']['hits']
    return (len(result))


def get_all_twitter_data(dict_name,page_number,page_size,start_date,end_date):
    start_from = (page_number-1)*page_size
    start_timestamps, end_timestamps = get_time(start_date, end_date)
    if start_timestamps==0 or end_timestamps == 0 :
        return None
    list = []
    for item in dict_name.keys():
        dict = {}
        dict["term"] = {"twitter_search":dict_name[item]}
        list.append(dict)
    query = {"query": {"bool": {"must": [{"range": {"timestamps": {"gt": start_timestamps, "lt": end_timestamps}}}], "must_not": [], "should": list}}, "from": start_from,
             "size": page_size, "sort": [], "aggs": {}}
    result = es.search(index=es_twitter_index, doc_type=es_twitter_type, body=query)['hits']['hits']
    list = []
    for item in result:
        dict = {}
        dict["context"] = item["_source"]["context"]
        dict["likes"] = item["_source"]["likes"]
        dict["name"] = item["_source"]["twitter_search"]
        dict["twitter_name"] = item["_source"]["twitter_name"]
        dict["comment"] = item["_source"]["comment"]
        dict["time"] = item["_source"]["time"].split(" ")[0]
        list.append(dict)
    return list

# if __name__ == '__main__':
#     dict = {}
#     dict[1]="卢秀燕"
#     dict[2]="林佳龙"
    # result = get_all_facebook_pages(dict,"2018-5-7","2018-5-7")
    # result = get_all_facebook_data(1,1,dict,"2018-5-7","2018-5-7")
    # result = get_facebook_pages("林佳龙","2018-5-7","2018-5-7")
    # result = get_facebook_data(1,1,"林佳龙","2018-5-7","2018-5-7")

    # result = get_all_news_pages(dict,"2018-5-7","2018-5-7")
    # result = get_all_news_data(1,1,dict,"2018-5-7","2018-5-7")
    # print (result)
    #
    # result = get_news_pages("林佳龙","2018-5-7","2018-5-7")
    # result = get_news_data(1,1,"林佳龙","2018-5-7","2018-5-7")
    # print (result)

    # result = get_all_twitter_pages(dict,"2018-5-7","2018-5-7")
    # result = get_all_twitter_data(1,1,dict,"2018-5-7","2018-5-7")
    # print (result)
    #
    # result = get_twitter_pages("林佳龙","2018-5-7","2018-5-7")
    # result = get_twitter_data(1,1,"林佳龙","2018-5-7","2018-5-7")
    # print (result)
