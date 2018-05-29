# coding=utf-8
from flask import jsonify,request
from . import mod
from monitor import app
from monitor.main.system.operate_info import insert_info,delete_info,update_info,select_info,get_is_candidate,get_region_dict,get_one_infos,select_candidate_facebook,add_administrative_infos,insert_candidate_facebook,delete_people_information
import json

#facebook写入数据
@mod.route('/insert/',methods=['POST'])
def insert():
    try:
        datas = request.form.get('data','')
        if len(datas) == 2:
            return jsonify({"message": "type input is null"}),406
        else:
            message = insert_info(json.loads(datas))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": message}),200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

#facebook删除数据
@mod.route('/delete/',methods=['POST'])
def delete():
    try:
        data = request.form.get('data','')
        if data == '':
            return  jsonify({"message": "type input is null"}),406
        else:
            message = delete_info(json.loads(data))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": message}),200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

#facebook修改数据
@mod.route('/update/',methods=['POST'])
def update():
    try:
        datas = request.form.get('data','')
        if datas == '':
            return  jsonify({"message": "type input is null"}),406
        else:
            message = update_info(json.loads(datas))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": message}),200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

#facebook查询数据
@mod.route('/select/',methods=['POST'])
def select():
    try:
        datas = request.form.get('data','')
        if datas == '':
            return  jsonify({"message": "type input is null"}),406
        else:
            message = select_info(json.loads(datas))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message":message}),200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


#查询候选人是否存在
#返回0 表示无，返回1 表示有，返回大于1 表示有重复数据，返回406表示输入的地区代码有错
@mod.route('/is_candidate/',methods=['POST'])
def is_candidate():
    try:
        datas = request.form.get('data','')
        if len(datas) < 3 or datas == '':
            return jsonify({"message": "data input is wrong"}), 406
        else:
            result = get_is_candidate(json.loads(datas))
            if result == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": result}),200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

#根据id查询单条信息
@mod.route('/one_select/',methods=['POST'])
def one_info():
    try:
        datas = request.form.get('data','')
        data = json.loads(datas)
        info_type = data.get('type')
        if info_type == '':
            return jsonify({"message": "type input is null"}), 406
        if data == '':
            return jsonify({"message": "data input is null"}), 406
        else:
            result = get_one_infos(info_type,data)
            if result == None:
                return jsonify({"message": "The data is wrong"}), 400
            else:
                return jsonify({"message": result}),200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

#地区代码字典
@mod.route('/region_dict/',methods = ['POST'])
def region_dict():
    try:
        data = request.form.get('data','')
        if data == '':
            return jsonify({"message": "type input is null"}),406
        else:
            result = get_region_dict(json.loads(data))
            if result == None:
                return jsonify({"message": "The region field is in the wrong"}), 400
            else:
                return jsonify({"message": result}),200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

#做分页
@mod.route('/get_pages/',methods = ['POST'])
def pages():
    data = request.form.get('data','')
    pass

#地区信息
def area_infos():
    pass

#增加候选人信息
@mod.route('/add_informations/',methods = ['POST'])
def add_information():
    try:
        datas = request.form.get("data","")
        data = json.loads(datas)
        if data == '' or len(data) == 0:
            return jsonify({"message":"data input is null"}),406
        else:
            if 'type' not in data or data['type'] == '':
                return jsonify({"message":"type input is null"}),406
            else:
                info_type = data.get('type')
                data.pop('type')
                select_insert_re = select_candidate_facebook(info_type,data)
                if select_insert_re == 1:
                    insert_re = insert_candidate_facebook(info_type,data)
                    if "数据" not in str(insert_re):
                        add_re = add_administrative_infos(insert_re,info_type,data)
                        if add_re == '' or add_re == None:
                            return jsonify({"message": "The data field is in the wrong"}), 400
                        else:
                            return jsonify({"message":add_re}),200
                    else:
                        return jsonify({"message":insert_re}),400
                else:
                    return jsonify({"message": select_insert_re}), 400
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

#修改候选人或者团队人员信息
@mod.route('/update_information/',methods=['POST'])
def update_information():
    try:
        datas = request.form.get('data','')
        data = json.loads(datas)
        info_type = data.get('type')
        if info_type == '':
            return jsonify({"message": "type input is null"}), 406
        if data == '':
            return jsonify({"message": "data input is null"}), 406
        else:
            result = delete_people_information(info_type,data)
            if result == None:
                return jsonify({"message": "The data is wrong"}), 400
            else:
                return jsonify({"message": result}),200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)



#删除候选人或者团队人员信息
@mod.route('/delete_information/',methods=['POST'])
def delete_information():
    try:
        datas = request.form.get('data','')
        data = json.loads(datas)
        info_type = data.get('type')
        if info_type == '':
            return jsonify({"message": "type input is null"}), 406
        if data == '':
            return jsonify({"message": "data input is null"}), 406
        else:
            result = delete_people_information(info_type,data)
            if result == None:
                return jsonify({"message": "The data is wrong"}), 400
            else:
                return jsonify({"message": result}),200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)
