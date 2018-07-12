# coding=utf-8
from flask import jsonify, request, url_for, send_from_directory, session

from monitor.main.system.candidate.candidate_infos import insert_info, update_info, delete_info, select_info, \
    get_is_candidate, get_one_infos, get_region_dict, get_pages, select_candidate_facebook, insert_candidate_facebook, \
    add_administrative_infos, update_people_information, delete_people_information, get_everyinformation, get_all_years, \
    get_new_id, allowed_file, update_image_name, del_arr_image, new_arr_image, change_arr_image
from . import mod
from monitor import app
import json, os
from monitor.util.mysql_util import closeAll

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
        print('1111')
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
        try:
            file = request.files['file']
        except:
            file = request.files.getlist('file_arr')
        # print(file)
        # print(info_type)
        # print('leader',leader)
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
                    return  jsonify({"message":"领导人图片名称未存储成功"}),200
        if info_type == '2':
            leader, member = get_new_id(info_type)
            image_name = str(leader) + '_' + str(member) + '.' + file.filename.rsplit('.', 1)[1]
            if file and allowed_file(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],image_name))
                update_image_re = update_image_name(info_type=info_type,image_name=image_name,ids=member)
                if update_image_re == 1:
                    return jsonify({"message": 1}), 201
                else:
                    return  jsonify({"message":"团队成员图片名称未存储成功"}),200
        if info_type == '3'and leader != None:#修改侯选人图片
            image_name = str(leader) + '.' + file.filename.rsplit('.', 1)[1]
            if file and allowed_file(file.filename):
                if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],image_name)):
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'],image_name))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],image_name),buffer_size=3145728)
                file.flush()
                os.fsync(file)
                file.close()
                update_image_re = update_image_name(info_type='1',image_name=image_name,ids=leader)
                if update_image_re == 1:
                    return jsonify({"message": 1}), 201
                else:
                    return  jsonify({"message":"侯选人图片名称未存储成功"}),200
        if info_type == '4'and leader != None and member != None:#修改团队人员图片
            image_name = str(leader) + '_' + str(member) + '.' + file.filename.rsplit('.', 1)[1]
            if file and allowed_file(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],image_name))
                update_image_re = update_image_name(info_type='2',image_name=image_name,ids=member)
                if update_image_re == 1:
                    return jsonify({"message": 1}), 201
                else:
                    return  jsonify({"message":"团队成员图片名称未存储成功"}),200
        if info_type == '5':#存储党派图片
            partisan_id = request.form.get('partisan_id','')
            if partisan_id != None and partisan_id != '':#修改图片
                if file and allowed_file(file.filename):
                    image_name = 'p_'+str(partisan_id) + '.' + file.filename.rsplit('.', 1)[1]
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],image_name ))
                    update_image_re = update_image_name(info_type=info_type,image_name=image_name,ids=partisan_id)
                    if update_image_re == 1:
                        return jsonify({"message": 1}), 201
                    else:
                        return  jsonify({"message":"党派图片名称未存储成功"}),200
            else:#添加党图片
                partisan = get_new_id(info_type)
                if file and allowed_file(file.filename):
                    image_name = 'p_'+str(partisan) + '.' + file.filename.rsplit('.', 1)[1]
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],image_name ))
                    update_image_re = update_image_name(info_type=info_type,image_name=image_name,ids=partisan)
                    if update_image_re == 1:
                        return jsonify({"message": 1}), 201
                    else:
                        return  jsonify({"message":"党派图片名称未存储成功"}),200
        if info_type == '6':
            image_infos = request.form.get('image_infos','')
            del_arr = request.form.getlist('del_arr[]')
            # print(type(del_arr))
            change_arr = request.form.getlist('change_arr[]')
            # print('del_arr',del_arr)
            # print('change_arr',change_arr)
            # print('image_infos',image_infos)
            num = 1
            new_file = ''
            change_file = ''
            cha = len(file) - len(change_arr)
            if len(change_arr) < len(file):
                begin = 0 -(len(file) - len(change_arr))
                new_file = file[begin:]
                change_file = file[:begin]
            if change_arr == [] :
                if del_arr ==[] and file == []:#未发生变化
                    # print('不变')
                    return jsonify({"message": 1}), 200
                if  del_arr != [] and file == []:#只删
                    # print('只删')
                    del_re = del_arr_image(del_arr,info_type,le=leader)
                    if del_re == 1:
                        return jsonify({"message":1}),200
                    else:
                        return  jsonify({"message":"侯选人图片删除失败"}),400
                if del_arr != []  and file != []:#删加
                    # print('删加')
                    new_re = new_arr_image(file,image_infos,info_type,le=leader)
                    if new_re == 1:
                        del_re = del_arr_image(del_arr,info_type,le=leader)
                        if del_re == 1:
                            return jsonify({"message":1}),200
                        else:
                            return  jsonify({"message":"侯选人图片删除失败"}),400
                    else:
                        return  jsonify({"message":"侯选人图片新增失败"}),400
                if del_arr == [] and file != []:#只加
                    # print('只加')
                    new_re = new_arr_image(file,image_infos,info_type,le=leader)
                    if new_re == 1:
                        return jsonify({"message":1}),201
                    else:
                        return  jsonify({"message":"侯选人图片新增失败"}),400
            elif change_arr != []:
                if del_arr != [] and file != [] and cha == 0:#删改
                    # print('删改')
                    cha_re = change_arr_image(file,change_arr,info_type)
                    if cha_re == 1:
                        del_re = del_arr_image(del_arr,info_type,le=leader)
                        if del_re == 1:
                            return jsonify({"message":1}),200
                        else:
                            return  jsonify({"message":"侯选人图片删除失败"}),400
                    else:
                        return  jsonify({"message":"侯选人图片删除成功，更新失败"}),400
                if file != [] and del_arr == [] and cha > 0:#改加
                    # print('改加')
                    new_re = new_arr_image(new_file,image_infos,info_type,le=leader)
                    if new_re == 1:
                        change_re = change_arr_image(change_file,change_arr,info_type)
                        if change_re == 1:
                            return jsonify({"message":1}),201
                        else:
                            return  jsonify({"message":"侯选人图片修改失败"}),400
                    else:
                        return  jsonify({"message":"侯选人图片新增失败"}),400
                if file != [] and del_arr == [] and cha == 0:#只改
                    # print('只改')
                    change_re = change_arr_image(file,change_arr,info_type)
                    if change_re == 1:
                        return jsonify({"message":1}),201
                    else:
                        return  jsonify({"message":"侯选人图片修改失败"}),400
                if file != [] and del_arr != [] and cha > 0:#删改加
                    # print('删改加')
                    change_re = change_arr_image(change_file,change_arr,info_type)
                    if change_re == 1:
                        new_re = new_arr_image(new_file,image_infos,info_type,le=leader)
                        if new_re == 1:
                            del_re = del_arr_image(del_arr,info_type,le=leader)
                            if del_re == 1:
                                return jsonify({"message":1}),200
                            else:
                                return  jsonify({"message":"侯选人图片删除失败"}),400
                        else:
                            return  jsonify({"message":"侯选人图片新增失败"}),400
                    else:
                        return  jsonify({"message":"侯选人图片修改失败"}),400
        if info_type == '7':
            image_infos = request.form.get('image_infos','')
            del_arr = request.form.getlist('del_arr[]')
            # print(type(del_arr))
            change_arr = request.form.getlist('change_arr[]')
            # print('del_arr',del_arr)
            # print('change_arr',change_arr)
            # print('image_infos',image_infos)
            num = 1
            new_file = ''
            change_file = ''
            cha = len(file) - len(change_arr)
            if len(change_arr) < len(file):
                begin = 0 -(len(file) - len(change_arr))
                new_file = file[begin:]
                change_file = file[:begin]
            if change_arr == [] :
                if del_arr ==[] and file == []:#未发生变化
                    # print('不变')
                    return jsonify({"message": 1}), 200
                if  del_arr != [] and file == []:#只删
                    # print('只删')
                    del_re = del_arr_image(del_arr,info_type,le=leader,me=member)
                    if del_re == 1:
                        return jsonify({"message":1}),200
                    else:
                        return  jsonify({"message":"侯选人团队成员图片删除失败"}),400
                if del_arr != []  and file != []:#删加
                    # print('删加')
                    new_re = new_arr_image(file,image_infos,info_type,le=leader,me=member)
                    if new_re == 1:
                        del_re = del_arr_image(del_arr,info_type,me=member)
                        if del_re == 1:
                            return jsonify({"message":1}),200
                        else:
                            return  jsonify({"message":"侯选人团队成员图片删除失败"}),400
                    else:
                        return  jsonify({"message":"侯选人团队成员图片新增失败"}),400
                if del_arr == [] and file != []:#只加
                    # print('只加')
                    new_re = new_arr_image(file,image_infos,info_type,le=leader,me=member)
                    if new_re == 1:
                        return jsonify({"message":1}),201
                    else:
                        return  jsonify({"message":"侯选人团队成员图片新增失败"}),400
            elif change_arr != []:
                if del_arr != [] and file != [] and cha == 0:#删改
                    # print('删改')
                    cha_re = change_arr_image(file,change_arr,info_type)
                    if cha_re == 1:
                        del_re = del_arr_image(del_arr,info_type,me=member)
                        if del_re == 1:
                            return jsonify({"message":1}),200
                        else:
                            return  jsonify({"message":"侯选人团队成员图片删除失败"}),400
                    else:
                        return  jsonify({"message":"侯选人团队成员图片删除成功，更新失败"}),400
                if file != [] and del_arr == [] and cha > 0:#改加
                    # print('改加')
                    new_re = new_arr_image(new_file,image_infos,info_type,le=leader,me=member)
                    if new_re == 1:
                        change_re = change_arr_image(change_file,change_arr,info_type)
                        if change_re == 1:
                            return jsonify({"message":1}),201
                        else:
                            return  jsonify({"message":"侯选人团队成员图片修改失败"}),400
                    else:
                        return  jsonify({"message":"侯选人团队成员图片新增失败"}),400
                if file != [] and del_arr == [] and cha == 0:#只改
                    # print('只改')
                    change_re = change_arr_image(file,change_arr,info_type)
                    if change_re == 1:
                        return jsonify({"message":1}),201
                    else:
                        return  jsonify({"message":"侯选人团队成员图片修改失败"}),400
                if file != [] and del_arr != [] and cha > 0:#删改加
                    # print('删改加')
                    change_re = change_arr_image(change_file,change_arr,info_type)
                    if change_re == 1:
                        new_re = new_arr_image(new_file,image_infos,info_type,le=leader,me=member)
                        if new_re == 1:
                            del_re = del_arr_image(del_arr,info_type,me=member)
                            if del_re == 1:
                                return jsonify({"message":1}),200
                            else:
                                return  jsonify({"message":"侯选人团队成员图片删除失败"}),400
                        else:
                            return  jsonify({"message":"侯选人团队成员图片新增失败"}),400
                    else:
                        return  jsonify({"message":"侯选人团队成员图片修改失败"}),400
    except Exception as erro:
        app.logger.error(erro)
        return str(0)


#存储侯选人和团队成员信息图片
def save_image_infos(file,image_name,image_infos,info_type,infos_id):
    update_image=image_infos+image_name
    update_image_re,conn,cur = update_image_name(info_type=info_type,image_name=update_image,ids=infos_id)
    if update_image_re == 1:
        if file and allowed_file(file.filename):
            try:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],image_name))
            except Exception as erro:
                app.logger.error(erro,'415行')
                conn.rollback()
                cur.close()
                conn.close()
                return 0
        closeAll(conn,cur)
        return jsonify({"message": 1}), 201
    else:
        return  jsonify({"message":"信息图片名称未存储成功"}),200