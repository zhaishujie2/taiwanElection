# coding=utf-8
from flask import jsonify, request, url_for, send_from_directory
from . import mod
from monitor import app
from monitor.main.system.operate_info import insert_info, delete_info, update_info, select_info, get_is_candidate, \
    get_region_dict, get_one_infos, select_candidate_facebook, add_administrative_infos, insert_candidate_facebook, \
    delete_people_information, update_people_information, get_everyinformation, get_all_years, get_pages, \
    allowed_file, \
    delete_area_info, insert_area_info, update_info_area, select_area_info, select_area_info_one, select_area_info_page, \
    insert_election_info, delete_election_info, update_election_info, select_election_all, select_election_info_one, \
    select_election_info_page, get_new_id, select_election_code_info, select_area_code_info, update_image_name, \
    select_support, delete_support, update_support, insert_support
import json, os


# facebook写入数据
@mod.route('/insert/', methods=['POST'])
def insert():
    try:
        datas = request.form.get('data', '')
        if len(datas) == 2:
            return jsonify({"message": "type input is null"}), 406
        else:
            message = insert_info(json.loads(datas))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": message}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# facebook删除数据
@mod.route('/delete/', methods=['POST'])
def delete():
    try:
        data = request.form.get('data', '')
        if data == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = delete_info(json.loads(data))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": message}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# facebook修改数据
@mod.route('/update/', methods=['POST'])
def update():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = update_info(json.loads(datas))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": message}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# facebook查询数据
@mod.route('/select/', methods=['POST'])
def select():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = select_info(json.loads(datas))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": message}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 查询候选人是否存在
# 返回0 表示无，返回1 表示有，返回大于1 表示有重复数据，返回406表示输入的地区代码有错
@mod.route('/is_candidate/', methods=['POST'])
def is_candidate():
    try:
        datas = request.form.get('data', '')
        if len(datas) < 3 or datas == '':
            return jsonify({"message": "data input is wrong"}), 406
        else:
            result = get_is_candidate(json.loads(datas))
            if result == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": result}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 根据id查询单条信息
@mod.route('/one_select/', methods=['POST'])
def one_info():
    try:
        datas = request.form.get('data', '')
        data = json.loads(datas)
        info_type = data.get('type')
        if info_type == '':
            return jsonify({"message": "type input is null"}), 406
        if data == '':
            return jsonify({"message": "data input is null"}), 406
        else:
            result = get_one_infos(info_type, data)
            if result == None:
                return jsonify({"message": "The data is wrong"}), 400
            else:
                return jsonify({"message": result}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 地区代码字典
@mod.route('/region_dict/', methods=['POST'])
def region_dict():
    try:
        data = request.form.get('data', '')
        if data == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            result = get_region_dict(json.loads(data))
            if result == None:
                return jsonify({"message": "The region field is in the wrong"}), 400
            else:
                return jsonify({"message": result}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 做分页
@mod.route('/pages/', methods=['POST'])
def pages():
    try:
        data = request.form.get('data','')
        datas = json.loads(data)
        result = get_pages(datas)
        if result == 0:
            return jsonify({"message": "The data is wrong "}), 400
        return jsonify({"message": result}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 增加候选人信息
@mod.route('/add_informations/', methods=['POST'])
def add_information():
    try:
        datas = request.form.get("data", "")
        data = json.loads(datas)

        if data == '' or len(data) == 0:
            return jsonify({"message": "data input is null"}), 406
        else:
            if 'type' not in data or data['type'] == '':
                return jsonify({"message": "type input is null"}), 406
            else:
                info_type = data.get('type')
                data.pop('type')
                select_insert_re = select_candidate_facebook(info_type, data)
                if select_insert_re == 1:
                    insert_re = insert_candidate_facebook(info_type, data)
                    if "数据" not in str(insert_re) and insert_re != 0:
                        add_re = add_administrative_infos(insert_re, info_type, data)
                        if add_re == '' or add_re == 0 or add_re == None:
                            return jsonify({"message": "The data field is in the wrong"}), 400
                        else:
                            return jsonify({"message": add_re}), 200
                    else:
                        return jsonify({"message": insert_re}), 400
                else:
                    return jsonify({"message": select_insert_re}), 400
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 修改候选人或者团队人员信息
@mod.route('/update_information/', methods=['POST'])
def update_information():
    try:
        datas = request.form.get('data', '')
        data = json.loads(datas)
        info_type = data.get('type')
        if info_type == '':
            return jsonify({"message": "type input is null"}), 406
        if data == '':
            return jsonify({"message": "data input is null"}), 406
        else:
            result = update_people_information(info_type, data)
            if result == None:
                return jsonify({"message": "The data is wrong"}), 400
            else:
                return jsonify({"message": result}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 删除候选人或者团队人员信息
@mod.route('/delete_information/', methods=['POST'])
def delete_information():
    try:
        datas = request.form.get('data', '')
        data = json.loads(datas)
        info_type = data.get('type')
        if info_type == '':
            return jsonify({"message": "type input is null"}), 406
        if data == '':
            return jsonify({"message": "data input is null"}), 406
        else:
            result = delete_people_information(info_type, data)
            if result == None:
                return jsonify({"message": "The data is wrong"}), 400
            else:
                return jsonify({"message": result}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 获取个人信息
@mod.route('/every_infos/', methods=['POST'])
def get_information():
    try:
        datas = request.form.get('data', '')
        data = json.loads(datas)
        info_type = data.get('type')
        content = data.get('content')
        if info_type == '' or info_type == None:
            return jsonify({"message": "type input is null"}), 406
        elif content == '' or content == None:
            return jsonify({"message": "data input is null"}), 406
        else:
            result = get_everyinformation(info_type, content)
            if result == 0:
                return jsonify({"message": "The data is wrong "}), 400
            return jsonify({"message": result}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 根据地区返回该地区的所有年份
@mod.route('/years_candidates/', methods=['POST'])
def years():
    try:
        datas = request.form.get('data', '')
        if datas == '' or datas == None:
            return jsonify({"message": "data input is null"}), 406
        else:
            data = json.loads(datas)
            info_type = data.get('type')
            result = get_all_years(info_type, data)
            if result == 0:
                return jsonify({"message": "The data is wrong "}), 400
            return jsonify({"message": result}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


@mod.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


# 上传图片
@mod.route('/image/', methods=['POST'])
def upload_file():
    try:
        info_type = request.form.get('type', '')
        member = request.form.get('id','')
        leader = request.form.get('candidate_id','')
        # leader = request.form.get('id','')
        file = request.files['file']
        if file == '' or file == None:
            return jsonify({"message": "data input is null"}), 406
        if info_type == '1':
            leader = get_new_id(info_type)
            if file and allowed_file(file.filename):
                image_name = str(leader) + '.' + file.filename.rsplit('.', 1)[1]
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],image_name ))
                update_image_re = update_image_name(info_type=info_type,image_name=image_name,ids=leader)
                if update_image_re == 1:
                    return jsonify({"message": 1}), 201
                else:
                    return  jsonify({"message":"图片名称未存储成功"}),400
        if info_type == '2':
            leader, member = get_new_id(info_type)
            image_name = str(leader) + '_' + str(member) + '.' + file.filename.rsplit('.', 1)[1]
            if file and allowed_file(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],image_name))
                update_image_re = update_image_name(info_type=info_type,image_name=image_name,ids=member)
                if update_image_re == 1:
                    return jsonify({"message": 1}), 201
                else:
                    return  jsonify({"message":"图片名称未存储成功"}),400
        if info_type == '3'and leader != None:#修改侯选人图片
            image_name = str(leader) + '.' + file.filename.rsplit('.', 1)[1]
            if file and allowed_file(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],image_name))
                update_image_re = update_image_name(info_type='1',image_name=image_name,ids=leader)
                if update_image_re == 1:
                    return jsonify({"message": 1}), 201
                else:
                    return  jsonify({"message":"图片名称未存储成功"}),400
        if info_type == '4'and leader != None and member != None:#修改团队人员图片
            image_name = str(leader) + '_' + str(member) + '.' + file.filename.rsplit('.', 1)[1]
            if file and allowed_file(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],image_name))
                update_image_re = update_image_name(info_type='2',image_name=image_name,ids=member)
                if update_image_re == 1:
                    return jsonify({"message": 1}), 201
                else:
                    return  jsonify({"message":"图片名称未存储成功"}),400
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 地区信息写入数据
@mod.route('/insert_area/',methods=['POST'])
def insert_area():
    try:
        datas = request.form.get('data', '')
        datas_info = json.loads(datas)
        administrative_id = datas_info.get('administrative_id')
        area_info = datas_info.get('area_info')
        governance_situation = datas_info.get('governance_situation')
        year = datas_info.get('year')

        if administrative_id and area_info and governance_situation and year:
            message = insert_area_info(administrative_id, area_info, governance_situation, year)
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400
        else:
            return jsonify({"message": "input info is not enough"}), 406

    except Exception as erro:
        app.logger.error(erro)
        return str(0)



# 地区信息删除数据
@mod.route('/delete_area/', methods=['POST'])
def delete_area():
    try:
        data = request.form.get('data', '')

        if data == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = delete_area_info(json.loads(data))
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400

    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 地区信息修改数据
@mod.route('/update_area/', methods=['POST'])
def update_area():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = update_info_area(json.loads(datas))
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400

    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 地区信息搜索所有数据
@mod.route('/select_area/',methods=['GET'])
def select_area():
    try:
        message, count = select_area_info()
        if message:
            return jsonify({"message": message, "count": count}), 200
        else:
            return jsonify({"message": "The data field is in the wrong", "count": count}), 400
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 地区信息根据id查询一条数据
@mod.route('/select_area_one/', methods=['POST'])
def select_area_one():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = select_area_info_one(json.loads(datas))
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 分页查询地区信息数据
@mod.route('/select_area_page/', methods=['POST'])
def select_area_page():
    try:
        datas = request.form.get('data', '')
        datas_info = json.loads(datas)
        page = datas_info['page']
        count = datas_info['count']

        if page and count:
            message = select_area_info_page(page, count)
            return jsonify({"message": message}), 200
        else:
            return jsonify({"message": "type input is null"}), 406
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 增加历届选举信息
@mod.route('/insert_election/', methods=['POST'])
def insert_election():
    try:
        datas = request.form.get('data', '')
        datas_info = json.loads(datas)
        administrative_id = datas_info.get('administrative_id')
        elector = datas_info.get('elector')
        election_score = datas_info.get('election_score')
        election_parties = datas_info.get('election_parties')
        period = datas_info.get('period')
        year = datas_info.get('year')

        if administrative_id and elector and election_score and election_parties and period and year:
            message = insert_election_info(administrative_id, elector, election_score, election_parties, period, year)
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400
        else:
            return jsonify({"message": "input info is not enough"}), 406

    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 删除历届选举信息
@mod.route('/delete_election/', methods=['POST'])
def delete_election():
    try:
        data = request.form.get('data', '')

        if data == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = delete_election_info(json.loads(data))
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400

    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 修改历届选举信息
@mod.route('/update_election/', methods=['POST'])
def update_election():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = update_election_info(json.loads(datas))
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400

    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 搜索全部历届选举信息
@mod.route('/select_election/',methods=['GET'])
def select_election():
    try:
        message, count = select_election_all()
        if message:
            return jsonify({"message": message, "count": count}), 200
        else:
            return jsonify({"message": "The data field is in the wrong", "count": count}), 400
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 根据id搜索一条选举信息
@mod.route('/select_election_one/', methods=['POST'])
def select_election_one():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = select_election_info_one(json.loads(datas))
            if message:
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400

    except Exception as erro:
        app.logger.error(erro)
        return str(0)


# 分页查询历届选举信息
@mod.route('/select_election_page/', methods=['POST'])
def select_election_page():
    try:
        datas = request.form.get('data', '')
        datas_info = json.loads(datas)
        page = datas_info['page']
        count = datas_info['count']

        if page and count:
            message = select_election_info_page(page, count)
            return jsonify({"message": message}), 200
        else:
            return jsonify({"message": "type input is null"}), 406
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

# 根据地区信息编码查询数据
@mod.route('/select_area_code/', methods=['POST'])
def select_area_code():
    try:
        datas = request.form.get('data','')
        datas_info = json.loads(datas)
        administrative_id = datas_info['administrative_id']
        page = datas_info['page']
        count_info = datas_info['count']

        if administrative_id and page and count_info:
            message, count = select_area_code_info(administrative_id, page, count_info)
            if message:
                return jsonify({"message": message, "count": count}), 200
            else:
                return jsonify({"message": "The data field is in the wrong", "count": count}, ), 400
        else:
            return jsonify({"message": "type input is null"}), 406

    except Exception as erro:
        app.logger.error(erro)
        return str(0)

# 根据地区编号搜索选举信息
@mod.route('/select_election_code/', methods=['POST'])
def select_election_code():
    try:
        datas = request.form.get('data', '')
        datas_info = json.loads(datas)
        administrative_id = datas_info['administrative_id']
        page = datas_info['page']
        count_info = datas_info['count']

        if administrative_id and page and count_info:
            message, count = select_election_code_info(administrative_id, page, count_info)
            if message:
                return jsonify({"message": message, "count": count}), 200
            else:
                return jsonify({"message": "The data field is in the wrong"}), 400
        else:
            return jsonify({"message": "type input is null"}), 406

    except Exception as erro:
        app.logger.error(erro)
        return str(0)


#获取民调数据
@mod.route('/select_support/',methods=['POST'])
def sele_support():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = select_support(json.loads(datas))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": message}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

#删除民调数据
@mod.route('/delete_support/',methods=['POST'])
def dele_support():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = delete_support(json.loads(datas))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": message}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

#修改民调数据
@mod.route('/update_support/',methods=['POST'])
def upda_support():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = update_support(json.loads(datas))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": message}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)

#添加民调数据
@mod.route('/insert_support/',methods=['POST'])
def inse_support():
    try:
        datas = request.form.get('data', '')
        if datas == '':
            return jsonify({"message": "type input is null"}), 406
        else:
            message = insert_support(json.loads(datas))
            if message == None:
                return jsonify({"message": "The data field is in the wrong"}), 400
            else:
                return jsonify({"message": message}), 200
    except Exception as erro:
        app.logger.error(erro)
        return str(0)
