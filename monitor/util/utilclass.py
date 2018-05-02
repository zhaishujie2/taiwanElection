#coding=utf-8
import time
import datetime
# 获取某天到当前天的时间戳
def get_time(day):
    end_day = datetime.datetime.now()
    end_time = int(time.mktime(datetime.datetime(end_day.year, end_day.month, end_day.day, 23, 59, 59).timetuple()))
    start_day = (datetime.date.today() - datetime.timedelta(days = day))
    start_time = int(time.mktime(datetime.datetime(start_day.year, start_day.month, start_day.day, 0, 0, 0).timetuple()))#    start_time = time.mktime(datetime.datetime(start_day.year, start_day.month, start_day.day, 0, 0, 0))#
    return start_time,end_time


