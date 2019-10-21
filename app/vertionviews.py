from flask import request, send_file, jsonify, make_response, session
import shutil
import re
import time
from uuid import uuid4
import threading
from app import app
from app.sqljob import TableManager
from app.softupdater import Updater
from app.pathinfo import *
from app.log2 import log
from app.log import log as sys_log
from app.softrefresh import markToRefresh
import app.user as user
from app.softpathmap import searchPathByStr, searchPathByRegex


# ##################################### Version #################################
@app.route('/api/ver/query', methods=['GET'])
def getVersion():
    '''
        根据请求的版本类型以及版本区间（不是数据库的id号）返回版本数据
        当某个版本类型下的所有版本数据按一定顺序（这里按名字降序排列）后，取
        位于第start_seq和end_seq之间的版本数据
        :return 格式如 {'itemsNum': 123, 'items': {'0': {'client': xxx, 'version': xxx , ...}, {'1': {...}}, ...}}

        * 2019.04.16: （Bug fix）当数据库中某一行数据被删除，再次遍历该数据时返回null，导致前端页面错误
    '''
    soft_type = request.args.get('softType')
    if soft_type not in ['V01', 'V02', 'V03V04', 'V05', 'T05']:
        return jsonify({'itemsNum': 0, 'items': {}})
    start_seq = int(request.args.get('start'))
    end_seq = int(request.args.get('end'))
    table_name = 't_' + soft_type
    t_soft = TableManager(table_name, SOFTWARE_VERSION_INFO_DB_PATH)
    all_ids = t_soft.getAllId('version', desc=True)
    ret_data = {'itemsNum': len(all_ids), 'items': {}}
    key = 0
    query_soft_num = end_seq - start_seq + 1
    for soft_id in all_ids[start_seq:]:
        if key >= query_soft_num:
            break
        temp_data = t_soft.displayDetailedData(soft_id)
        if not temp_data:
            continue
        ret_data['items'][key] = temp_data
        key += 1

    return jsonify(ret_data)

# 需要遍历数据库和xls表，并且对比两者的差别，非常费时
# 检测更新需要遍历数据库和xls表，为了避免确认更新时，重复检测更新
# 将下面变量设为全局变量
updaters = {
    'V01': Updater('t_V01', 'V01'),
    'V02': Updater('t_V02', 'V02'),
    'V03V04': Updater('t_V03V04', 'V03&V04'),
    'V05': Updater('t_V05', 'V05'),
    'T05': Updater('t_T05', 'T05'),
}
@app.route('/api/ver/checkupdate', methods=['GET'])
def checkUpdate():
    '''
        检查某类版本的更新信息
        如果找不到或无法打开'软件版本登记表.xls'文件，这里返回状态为失败。
        :return: 成功返回格式如 {'status': success, 'info': {"new": [{'client': xx, 'version': xx, ...}, {...}, ,,]}
                  失败返回格式如 {'status': failure, 'description': 'xxxx'}
    '''
    global updaters
    soft_type = request.args.get('softType')
    vers_ready_to_update = updaters[soft_type].getUpdateInfo()
    if vers_ready_to_update == -1:
        return jsonify({'status': 'failure', 'description': '无法打开xls文件路径或xls文件内没有正确的sheet，检查后台 "软件版本登记表.xls" 文件路径'})
    elif vers_ready_to_update == 0:
        return jsonify({'status': 'failure', 'description': '其他线程正在更新数据，稍后刷新重试'})
    return jsonify({'status': 'success', 'info': vers_ready_to_update})

@app.route('/api/ver/startupdate', methods=['GET'])
def startUpdate():
    global updaters
    soft_type = request.args.get('softType')
    client_ip = request.remote_addr
    record_info = 'IP: ' + client_ip + '更新软件版本'
    record_info += str(updaters[soft_type].vers_ready_to_update)
    log.record(ip=client_ip, event="更新软件版本", description=str(updaters[soft_type].vers_ready_to_update), username="")

    if updaters[soft_type].startUpdate() is False:
        return jsonify({'status': 'failure', 'description': '更新信息已过期或后台繁忙，请重试'})
    return jsonify({'status': 'success'})

@app.route('/api/ver/downloadsrccode', methods=['GET'])
def downloadSrcCode():
    '''
        为网页端准备下载文件（根据提供的路径复制文件到cache/），然后返回url提供下载
    '''
    src_path = request.args.get('path')
    if not os.path.isfile(src_path):
        return jsonify({'status': 'failure', 'description': '数据库路径无效在本服务器上无效，'})
    file_name = os.path.basename(src_path)
    dst_path = os.path.join(CACHE_FILE_DIR, file_name)
    if os.path.isfile(dst_path):
        # 如果该文件原来已经被复制到cache目录下，则直接返回该文件路径
        src_code_url = os.path.join(URL_DIR, file_name)
        return jsonify({'status': 'success', 'url': src_code_url})
    try:
        # 如果src_path和dst_path指向同一个文件，会导致复制失败
        shutil.copy(src_path, dst_path)
    except Exception as e:
        sys_log.record(str(e))
        return jsonify({'status': 'failure', 'description': '后台源程序文件复制失败，请重试'})
    src_code_url = os.path.join(URL_DIR, file_name)
    return jsonify({'status': 'success', 'url': src_code_url})

@app.route('/api/ver/searchversions', methods=['GET'])
def searchVersion():
    search_str = request.args.get('text')
    client_ip = request.remote_addr
    log.record(ip=client_ip, event="搜索", description=search_str, username="")
    ret_data = {'itemsNum': 0, 'items': {}}
    if search_str == '':
        return jsonify(ret_data)
    t_vers = {
        'V01': TableManager('t_V01', SOFTWARE_VERSION_INFO_DB_PATH),
        'V02': TableManager('t_V02', SOFTWARE_VERSION_INFO_DB_PATH),
        'V03V04': TableManager('t_V03V04', SOFTWARE_VERSION_INFO_DB_PATH),
        'V05': TableManager('t_V05', SOFTWARE_VERSION_INFO_DB_PATH),
        'T05': TableManager('t_T05', SOFTWARE_VERSION_INFO_DB_PATH)
    }
    keywords = re.split(r'\s+', search_str)
    key = 0
    ver_list = []
    for soft_type in t_vers:
        ids_for_each_keyword = []

        for keyword in keywords:
            # 在表中搜索1个关键字
            ids_for_each_keyword.append(t_vers[soft_type].searchDataInTable(keyword, 'path'))
        # 取多个关键字获得到重合id部分，即筛选出符合多个条件的数据
        ids = ids_for_each_keyword[0]
        for i in range(1, len(ids_for_each_keyword)):
            ids = tuple(soft_id for soft_id in ids if soft_id in ids_for_each_keyword[i])
        ret_data['itemsNum'] += len(ids)
        # for soft_id in ids:
            # ret_data['items'][key] = t_vers[soft_type].displayDetailedData(soft_id)
            # key += 1
        for soft_id in ids:
            ver_list.append(t_vers[soft_type].displayDetailedData(soft_id))
    # 将搜索得到的版本号进行降序排序
    ver_list = sorted(ver_list, key=lambda x: x['version'], reverse=True)
    seq_list = list(i for i in range(1, ret_data['itemsNum'] + 1))
    ret_data['items'] = dict(zip(seq_list, ver_list))
    return jsonify(ret_data)

@app.route('/api/ver/referversions', methods=['GET'])
def referVersion():
    search_str = request.args.get('ver')
    ret_data = {'itemsNum': 0, 'items': {}}
    ver_list = []
    t_vers = {
        'V01': TableManager('t_V01', SOFTWARE_VERSION_INFO_DB_PATH),
        'V02': TableManager('t_V02', SOFTWARE_VERSION_INFO_DB_PATH),
        'V03V04': TableManager('t_V03V04', SOFTWARE_VERSION_INFO_DB_PATH),
        'V05': TableManager('t_V05', SOFTWARE_VERSION_INFO_DB_PATH),
        'T05': TableManager('t_T05', SOFTWARE_VERSION_INFO_DB_PATH)
    }
    next_search_vers = [search_str]
    while True:
        # 向之前的版本遍历，只需搜索"版本"
        if not next_search_vers:
            break
        cur_search_vers = next_search_vers.copy()
        next_search_vers = []
        for cur_search_ver in cur_search_vers:
            for soft_type in t_vers:
                ids = t_vers[soft_type].searchDataByKey(strict=True, version=cur_search_ver)
                for soft_id in ids:
                    temp = t_vers[soft_type].displayDetailedData(soft_id)
                    ver_list.append(temp)
                    next_search_vers.append(temp['base'])
    next_search_vers = [search_str]
    while True:
        # 向之后的版本遍历，只需搜索"原版本"
        if not next_search_vers:
            break
        cur_search_vers = next_search_vers.copy()
        next_search_vers = []
        for soft_type in t_vers:
            for cur_search_ver in cur_search_vers:
                ids = t_vers[soft_type].searchDataByKey(strict=True, base=cur_search_ver)
                for soft_id in ids:
                    temp = t_vers[soft_type].displayDetailedData(soft_id)
                    ver_list.append(temp)
                    next_search_vers.append(temp['version'])
    ver_list = sorted(ver_list, key=lambda x: x['version'], reverse=True)
    ret_data['itemsNum'] = len(ver_list)
    seq_list = list(i for i in range(1, ret_data['itemsNum'] + 1))
    ret_data['items'] = dict(zip(seq_list, ver_list))
    return jsonify(ret_data)


@app.route('/api/ver/submiterror', methods=['GET'])
def submitError():
    soft_type = request.args.get('type')
    err_id = request.args.get('id')
    # 将用户提交的错误错误路径版本进行标记（torefresh字段写1）
    table_name = 't_' + soft_type
    markToRefresh(table_name, int(err_id))
    # 记录日志
    client_ip = request.remote_addr
    log.record(ip=client_ip, event="标记路径问题", description=soft_type + ":" + err_id, username="")
    return jsonify({'status': 'success'})

@app.route('/api/ver/checkallupdate', methods=['GET'])
def checkAllUpdate():
    '''
        检查所有版本的更新信息
        :return: {"V01": {
                        "status": "success",
                        "info": {
                            "new": {"client": "xxx", ...},
                            "expire": {"client": "xxx", xxx}
                            }
                        },
                    "V02": {...}, ...
                    }
    '''
    global updaters
    ret_val = {}
    for soft_type, updater in updaters.items():
        update_info = updater.getUpdateInfo()
        if update_info == -1:
            ret_val[soft_type] = {'status': 'failure', 'description': '无法打开xls文件路径或xls文件内没有正确的sheet，检查后台 "软件版本登记表.xls" 文件路径'}
        elif update_info == -2:
            ret_val[soft_type] = {'status': 'failure', 'description': '其他线程正在更新数据，稍后刷新重试'}
        else:
            ret_val[soft_type] = {'status': 'success', 'info': update_info}
    return jsonify(ret_val)

@app.route('/api/ver/releasenote', methods=['GET'])
def getReleaseNote():
    ret_data = {'status': True, 'releaseNote': {}}
    t_std_ver = TableManager('t_vers', STD_SOFTWARE_RELEASE_NOTE_DB_PATH)
    ids = t_std_ver.getAllId(orderby="version", desc=True)
    ver_count = 0
    for each_id in ids:
        # 使用ver_count保证json数据按版本号降序排列
        ver_count += 1
        ver_info = t_std_ver.displayBriefData(each_id, "version", "origin", "release_note")
        ret_data['releaseNote'][ver_count] = {}
        ret_data['releaseNote'][ver_count]['id'] = each_id
        ret_data['releaseNote'][ver_count]['version'] = ver_info[0]
        ret_data['releaseNote'][ver_count]['origin'] = ver_info[1]
        ret_data['releaseNote'][ver_count]['releaseNote'] = ver_info[2].split(';;;')
    return jsonify(ret_data)

@app.route('/api/version/modifyreleasenote', methods=['POST'])
def modifyReleaseNote():
    ver_info = request.get_json()
    client_ip = request.remote_addr
    account = request.cookies.get('account')
    sp = request.cookies.get('sp')
    ssid = request.cookies.get('ssid')
    ret_data = {"status": False, "description": ""}
    if user.verifyCookies(account, sp, ssid) and sp == '1':
        try:
            release_note_arr = list(map(lambda x: x.replace(';;;', ':::'), ver_info['releaseNote']))
            t_std_ver = TableManager('t_vers', STD_SOFTWARE_RELEASE_NOTE_DB_PATH)
            ver_info_in_db = t_std_ver.displayDetailedData(ver_info['id'])
            t_std_ver.modifyLine(ver_info['id'], version=ver_info['version'], origin=ver_info['origin'], release_note=';;;'.join(release_note_arr))
            ret_data["status"] = True
            log.record(ip=client_ip, event="更新ReleaseNote", description="原数据"+str(ver_info_in_db), username=account)
        except Exception as e:
            print(e)
            ret_data["description"] = "服务器遇到问题，请见系统日志"
            sys_log.record(str(e))
    else:
        ret_data["description"] = "你没有权限修改，或者重新登录后尝试再次提交"
    return jsonify(ret_data)

@app.route('/api/version/newnote', methods=['POST'])
def getNewReleaseNote():
    ver_info = request.get_json()
    client_ip = request.remote_addr
    account = request.cookies.get('account')
    sp = request.cookies.get('sp')
    ssid = request.cookies.get('ssid')
    ret_data = {"status": False, "description": ""}
    if user.verifyCookies(account, sp, ssid) and sp == '1':
        try:
            t_std_ver = TableManager('t_vers', STD_SOFTWARE_RELEASE_NOTE_DB_PATH)
            release_note_arr = list(map(lambda x: x.replace(';;;', ':::'), ver_info['releaseNote']))
            t_std_ver.appendLine(version=ver_info['version'], origin=ver_info['origin'], release_note=';;;'.join(release_note_arr))
            ret_data["status"] = True
            log.record(ip=client_ip, event="增加ReleaseNote", description="新数据"+str(ver_info), username=account)
        except Exception as e:
            sys_log.record(str(e))
            ret_data["description"] = "服务器遇到问题，请见系统日志"
            return jsonify(ret_data)
    else:
        ret_data["description"] = "你没有权限修改，或者重新登录后尝试再次提交"
    return jsonify(ret_data)

@app.route('/api/version/delnote', methods=['POST'])
def delReleaseNote():
    ver_info = request.get_json()
    client_ip = request.remote_addr
    account = request.cookies.get('account')
    sp = request.cookies.get('sp')
    ssid = request.cookies.get('ssid')
    ret_data = {"status": False, "description": ""}
    if user.verifyCookies(account, sp, ssid) and sp == '1':
        try:
            t_std_ver = TableManager('t_vers', STD_SOFTWARE_RELEASE_NOTE_DB_PATH)
            ver_info_in_db = t_std_ver.displayDetailedData(ver_info['id'])
            t_std_ver.deleteLine(ver_info['id'])
            ret_data["status"] = True
            log.record(ip=client_ip, event="删除ReleaseNote", description="原数据"+str(ver_info_in_db), username=account)
        except Exception as e:
            sys_log.record(str(e))
            ret_data["description"] = "服务器遇到问题，请见系统日志"
            return jsonify(ret_data)
    else:
        ret_data["description"] = "你没有权限修改，或者重新登录后尝试再次提交"
    return jsonify(ret_data)

# 用来存储搜索过程中的数据
search_result = {}
@app.route('/api/ver/startdisksearch', methods=['POST'])
def startDiskSearch():
    search_info = request.get_json()
    searching_key = search_info['key']
    searching_mode = search_info['mode']
    client_ip = request.remote_addr
    log.record(ip=client_ip, event="磁盘搜索", description=searching_key, username="")
    disk_search_id = str(uuid4())
    # search_result中每个元素的的结构格式如下
    search_slot = {'terminate': False, 'progress': [], 'num': 0}
    search_result[disk_search_id] = {"key": searching_key,
                                     "slot": search_slot,
                                     "status": False,
                                     "starting_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                     "mode": searching_mode}
    def _startSearch(mode):
        if str(mode) == "0":
            # 普通搜索模式
            searchPathByStr(searching_key, search_slot)
        else:
            # 正则搜索
            searchPathByRegex(searching_key, search_slot)
        search_result[disk_search_id]['status'] = True
    thread_search = threading.Thread(target=_startSearch, args=(searching_mode, ))
    thread_search.start()
    ret_data = {'status': True, 'id': disk_search_id}
    return jsonify(ret_data)

@app.route('/api/ver/getdisksearchprogress', methods=['GET'])
def getDiskSearchProgress():
    client_ip = request.remote_addr
    disk_search_id = request.args.get('id')
    ret_data = {"status": False, "progress": [], 'num': 0}
    if disk_search_id not in search_result:
        return jsonify(ret_data)
    ret_data["status"] = search_result[disk_search_id]["status"]
    ret_data["progress"] = search_result[disk_search_id]["slot"]["progress"]
    ret_data["num"] = search_result[disk_search_id]["slot"]["num"]
    if search_result[disk_search_id]["status"]:
        if len(search_result[disk_search_id]["slot"]["progress"]) > 20:
            # 如果搜索结果太多，全部记录到数据库，下次全部读取会导致浏览器内存耗尽
            log.record(ip=client_ip, event="全盘搜索", description="结果太多，无法存入数据库", username="")
        else:
            log.record(ip=client_ip, event="全盘搜索", description=str(search_result[disk_search_id]), username="")
        # 虽然pop掉了，但是信息还是保存在了ret_data中，
        # 猜测在pop时，如果存在多个引用，只是删掉了引用；如果只有1个引用，就清内存了
        search_result.pop(disk_search_id)
    return jsonify(ret_data)

@app.route("/api/ver/getdisksearchthreads", methods=['GET'])
def getDiskSearchThreads():
    return jsonify(search_result)

@app.route("/api/ver/stopdisksearchthread", methods=['GET'])
def stopDiskSearchThread():
    client_ip = request.remote_addr
    disk_search_id = request.args.get('id')
    ret_data = {"status": False, "description": ""}
    if disk_search_id not in search_result:
        ret_data["description"] = "搜索id已失效"
        return jsonify(ret_data)
    search_result[disk_search_id]["slot"]["terminate"] = True
    search_result[disk_search_id]["status"] = True
    ret_data["status"] = True
    ret_data["description"] = disk_search_id + " 已经停止"
    log.record(ip=client_ip, event="结束搜索", description=disk_search_id, username="")
    return jsonify(ret_data)
