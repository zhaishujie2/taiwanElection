from monitor.util.config import es_host,es_news_index,es_news_type
from elasticsearch import Elasticsearch
es = Elasticsearch(es_host, timeout=600)
def taiwan_latest_news(count):
    try:
        query = {"query": {"bool": {"must": [{"match_all": {}}]}}, "from": 0, "size": count,
                 "sort": [{"time": {"order": "desc"}}]}
        result = es.search(index=es_news_index, doc_type=es_news_type, body=query)['hits']['hits']
        list  = []
        for item in result:
            dict = {}
            dict["title"] = item["_source"]["title"]
            dict["context"] = item["_source"]["context"]
            dict["source"] = item["_source"]["news_source"]
            dict["summary"] = item["_source"]["summary"]
            dict["time"] = item["_source"]["time"]
            list.append(dict)
        return list
    except:
        return 0

def taiwan_event_news(count):
    try:
        query = {"query": {"bool": {"must": [{"match_all": {}}]}}, "from": 20, "size": count,
                 "sort": [{"time": {"order": "desc"}}]}
        result = es.search(index=es_news_index, doc_type=es_news_type, body=query)['hits']['hits']
        list  = []
        for item in result:
            dict = {}
            dict["title"] = item["_source"]["title"]
            dict["context"] = item["_source"]["context"]
            dict["source"] = item["_source"]["news_source"]
            dict["summary"] = item["_source"]["summary"]
            dict["time"] = item["_source"]["time"]
            list.append(dict)
        return list
    except:
        return 0
