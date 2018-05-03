# coding=utf-8
from flask import request, session
from .draw_mysql import get_map_color,get_egional_electors
from monitor import app
from . import mod
import json

# 获取地图颜色信息
@mod.route('/get_map/')
def get_map():
    year = request.args.get('year', '')
    if year == None:
        app.logger.error("年份传入错误")
        return "0"
    else:
        app.logger.info("获取"+year+"年的政党信息")
        result = get_map_color(int(year))
        return  json.dumps(result)

@mod.route('/record_session/',methods=['POST'])
def record_session():
    id = request.form.get('id', '')
    year = request.form.get('year', '')
    if id !='' and year!='':
        user_dict = get_egional_electors(int(id),int(year))
        if user_dict!=0:
            session["electors"] = json.dumps(user_dict)
            session["year"] = year
            session["area_id"] = id
            return "1"
        else:
            return "0"
    else:
        app.logger.error("传入area_id,year有误 id:"+id+"year:"+year)
        return "0"