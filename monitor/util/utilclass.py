#coding=utf-8
import time
import datetime
# 获取某天到当前天的时间戳
def get_time(start_time,end_time):
    try:
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d')
        end_time = int(time.mktime(datetime.datetime(end_time.year, end_time.month, end_time.day, 23, 59, 59).timetuple()))
        start_time = int(time.mktime(datetime.datetime(start_time.year, start_time.month, start_time.day, 0, 0, 0).timetuple()))#    start_time = time.mktime(datetime.datetime(start_day.year, start_day.month, start_day.day, 0, 0, 0))#
        return start_time,end_time
    except:
        return 0,0

def get_date(start_time,end_time):
    try:
        d1 = datetime.datetime.strptime(start_time, '%Y-%m-%d')
        d2 = datetime.datetime.strptime(end_time, '%Y-%m-%d')
        list = []
        list.append(d1.strftime("%Y-%m-%d"))
        count = d2-d1
        count = count.days
        for i in range(1,count):
            d3 = d1+datetime.timedelta(days=i)
            list.append(d3.strftime("%Y-%m-%d"))
        list.append(d2.strftime("%Y-%m-%d"))
        return list
    except:
        return 0

def get_date_item(date_time):
    return datetime.datetime.strptime(date_time, '%Y-%m-%d')

def get_timestamps_to_date(timestamps):
    return datetime.datetime.fromtimestamp(timestamps).strftime('%Y-%m-%d')

#获得几天前的日期
def get_before_time(tiem,day):
    d1 = datetime.datetime.strptime(tiem, '%Y-%m-%d')
    start_time = d1-datetime.timedelta(days=day)
    return start_time.strftime("%Y-%m-%d")

if __name__ == '__main__':
    list = get_time("2018-5-1","2018-5-7")
    print (list)