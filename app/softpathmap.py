import re
import shutil
from app.sqljob import TableManager
from app.pathinfo import *


def _searchVerInStr(ver, str):
    '''
        在字符串str中搜索匹配是否包含相应的版本信息ver
        :param ver: 版本信息，例如'v05_38_01'或'V05-38-01'，只允许是以'-'或'_'分隔的版本信息
        :param str: 可能包含该版本信息的字符串，如'AkV05-38-91_1_piabc'
        :return: re.search()的结果，可以直接按boolean方式判断
    '''
    if ver.upper().startswith('V'):
        ver = ver.strip('Vv')
        re_str = '[^t]' + '[-_]+'.join(re.split(r'[-_]+', ver))
    else:
        # T开头的版本
        re_str = '[-_]+'.join(re.split(r'[-_]+', ver))
    return re.search(re_str, str, re.IGNORECASE)

def _createVersDict():
    '''
        从数据库文件获取到所有的软件版本，返回一个dict变量，里面不包含任何path信息
        :return: 格式如
        {
            'V01': {1: {'version': 'V01_17_16}, 'path': ''}, 2: {xxx}, ...,},
            'V02': {1: {}, 2: {}, ...}
            ...
        }
    '''
    vers_dict = {'V01': {},
                 'V02': {},
                 'V03V04': {},
                 'V05': {},
                 'T05': {}
                 }
    t_vers = {
        'V01': TableManager('t_V01', SOFTWARE_VERSION_INFO_DB_PATH),
        'V02': TableManager('t_V02', SOFTWARE_VERSION_INFO_DB_PATH),
        'V03V04': TableManager('t_V03V04', SOFTWARE_VERSION_INFO_DB_PATH),
        'V05': TableManager('t_V05', SOFTWARE_VERSION_INFO_DB_PATH),
        'T05': TableManager('t_T05', SOFTWARE_VERSION_INFO_DB_PATH)
    }
    for key in vers_dict:
        for id in t_vers[key].getAllId():
            ver = t_vers[key].displayBriefData(id, 'version')[0]
            vers_dict[key][id] = {'version': ver, 'path': ''}
    return vers_dict

def _createEmptyPathVersDict():
    '''
        从数据库中获取出所有path字段为空的数据
        :return: 格式如
        {
            'V01': {1: {'version': 'V01_17_16}, 'path': ''}, 2: {xxx}, ...,},
            'V02': {1: {}, 2: {}, ...}
            ...
        }
    '''
    ver_path_map = {'V01': {},
                    'V02': {},
                    'V03V04': {},
                    'V05': {},
                    'T05': {}
                    }
    t_vers = {
        'V01': TableManager('t_V01', SOFTWARE_VERSION_INFO_DB_PATH),
        'V02': TableManager('t_V02', SOFTWARE_VERSION_INFO_DB_PATH),
        'V03V04': TableManager('t_V03V04', SOFTWARE_VERSION_INFO_DB_PATH),
        'V05': TableManager('t_V05', SOFTWARE_VERSION_INFO_DB_PATH),
        'T05': TableManager('t_T05', SOFTWARE_VERSION_INFO_DB_PATH)
    }
    for key in ver_path_map:
        for id in t_vers[key].getAllId():
            ver, path = t_vers[key].displayBriefData(id, 'version', 'path')
            if ver != '' and (not path or path == ''):
                ver_path_map[key][id] = {'version': ver, 'path': ''}
    return ver_path_map

def getAllVerPathInfo():
    '''
        从数据库文件获取到所有的软件版本及对应的path信息，返回一个dict变量
        :return: 格式如
        {
            'V01': {1: {'version': 'V01_17_16}, 'path': 'G:/sigmatek/...'}, 2: {xxx}, ...,},
            'V02': {1: {}, 2: {}, ...}
            ...
        }
    '''
    ver_path_map = {'V01': {},
                 'V02': {},
                 'V03V04': {},
                 'V05': {},
                 'T05': {}
                 }
    t_vers = {
        'V01': TableManager('t_V01', SOFTWARE_VERSION_INFO_DB_PATH),
        'V02': TableManager('t_V02', SOFTWARE_VERSION_INFO_DB_PATH),
        'V03V04': TableManager('t_V03V04', SOFTWARE_VERSION_INFO_DB_PATH),
        'V05': TableManager('t_V05', SOFTWARE_VERSION_INFO_DB_PATH),
        'T05': TableManager('t_T05', SOFTWARE_VERSION_INFO_DB_PATH)
    }
    for key in ver_path_map:
        for id in t_vers[key].getAllId():
            ver, path = t_vers[key].displayBriefData(id, 'version', 'path')
            ver_path_map[key][id] = {'version': ver, 'path': path}
    return ver_path_map

def mapAllVersionsPath():
    '''
        为soft.db内存放的所有软件版本搜索源程序文件路径。
        该方法会遍历SOFTWARE_SRC_CODE_DIR目录下所有的文件，
        其中文件名为 *.zip, *.rar, *.7z 会进行所有版本进行正则匹配（指定后缀名以加快搜索速度）
        该方法内部循环次数为 (SOFTWARE_SRC_CODE_DIR目录下文件数 * software_version的数量)
        返回一个dict变量，包含软件版本号及匹配后对应的文件路径信息
        :return: 格式如
        {
            'V01': {1: {'version': 'V01_17_16}, 'path': 'G:/sigmatek/...'}, 2: {xxx}, ...,},
            'V02': {1: {}, 2: {}, ...}
            ...
        }
    '''
    ver_path_map = _createVersDict()
    print('Start search...')
    count = 0
    # 带匹配的文件名
    target_ext = ['.RAR', '.7Z', '.ZIP']
    for root, dirs, files in os.walk(SOFTWARE_SRC_CODE_DIR):
        for file in files:
            # 遍历目录下所有的文件
            try:
                # 某些文件名瞎JB命名，Python无法解析，可能导致程序以外终止！
                ext = os.path.splitext(file)[1].upper()
                if ext not in target_ext:
                    continue
                print(file, '正在比较.....')
            except:
                continue
            for ver_type in ver_path_map:
                # ver_type的格式为{1: {'version': 'V01_17_16}, 'path': ''}, 2: {xxx}, ...,}
                for ver_id, ver_info in ver_path_map[ver_type].items():
                    if _searchVerInStr(ver_info['version'], file):
                        this_ver_path = os.path.join(root, file)
                        if ver_info['path'] == '':
                            ver_info['path'] = this_ver_path
                        else:
                            ver_info['path'] += ';' + this_ver_path
                        print(this_ver_path)
                        count += 1
    print('Success, found %d files' % count)
    # 移除path信息仍为''的数据
    for ver_type in ver_path_map:
        # 如果采用常规遍历dict方法删除空path项目，会导致程序报错
        for ver_id in list(ver_path_map[ver_type].keys()):
            if ver_path_map[ver_type][ver_id]['path'] == '':
                del ver_path_map[ver_type][ver_id]
    return ver_path_map

def mapEmptyPathVersionsPath():
    '''
        为soft.db内存放的未写入path信息的软件版本搜索源程序文件路径。
        该方法会遍历SOFTWARE_SRC_CODE_DIR目录下所有的文件，
        其中文件名为 *.zip, *.rar, *.7z 会进行所有版本进行正则匹配（指定后缀名以加快搜索速度）
        该方法内部循环次数为 (SOFTWARE_SRC_CODE_DIR目录下文件数 * software_version的数量)
        返回一个dict变量，包含软件版本号及匹配后对应的文件路径信息
        :return: 格式如
        {
            'V01': {1: {'version': 'V01_17_16}, 'path': 'G:/sigmatek/...'}, 2: {xxx}, ...,},
            'V02': {1: {}, 2: {}, ...}
            ...
        }
    '''
    ver_path_map = _createEmptyPathVersDict()
    print('Start search...')
    count = 0
    # 带匹配的文件名
    target_ext = ['.RAR', '.7Z', '.ZIP']
    for root, dirs, files in os.walk(SOFTWARE_SRC_CODE_DIR):
        for file in files:
            # 遍历目录下所有的文件
            try:
                # 某些文件名瞎JB命名，Python无法解析，可能导致程序以外终止！
                ext = os.path.splitext(file)[1].upper()
                if ext not in target_ext:
                    continue
                print(file, '正在比较.....')
            except:
                continue
            for ver_type in ver_path_map:
                # ver_path_map[ver_type]的格式为{1: {'version': 'V01_17_16}, 'path': ''}, 2: {xxx}, ...,}
                for ver_id, ver_info in ver_path_map[ver_type].items():
                    if _searchVerInStr(ver_info['version'], file):
                        this_ver_path = os.path.join(root, file)
                        if ver_info['path'] == '':
                            ver_info['path'] = this_ver_path
                        else:
                            ver_info['path'] += ';' + this_ver_path
                        print(this_ver_path)
                        count += 1
    print('Success, found %d files' % count)
    # 移除path信息仍为''的数据
    for ver_type in ver_path_map:
        # 如果采用常规遍历dict方法删除空path项目，会导致程序报错
        for ver_id in list(ver_path_map[ver_type].keys()):
            if ver_path_map[ver_type][ver_id]['path'] == '':
                del ver_path_map[ver_type][ver_id]
    print(ver_path_map)
    return ver_path_map


def writeAllPathInfo(ver_path_map):
    '''
        把新的版本--路径信息写入到数据库，会覆盖原先数据库中的path信息
        :param ver_path_map: 格式如
        {
            'V01': {1: {'version': 'V01_17_16}, 'path': 'G:/sigmatek/...'}, 2: {xxx}, ...,},
            'V02': {1: {}, 2: {}, ...}
            ...
        }
        :return:
    '''
    # 提前备份一个soft.db文件，万一写烂给留条后路撤退
    db_cpy_name = 'soft_cpy.db'
    db_cpy_path = os.path.join(os.path.dirname(SOFTWARE_VERSION_INFO_DB_PATH), db_cpy_name)
    shutil.copyfile(SOFTWARE_VERSION_INFO_DB_PATH, db_cpy_path)
    t_vers = {
        'V01': TableManager('t_V01', SOFTWARE_VERSION_INFO_DB_PATH),
        'V02': TableManager('t_V02', SOFTWARE_VERSION_INFO_DB_PATH),
        'V03V04': TableManager('t_V03V04', SOFTWARE_VERSION_INFO_DB_PATH),
        'V05': TableManager('t_V05', SOFTWARE_VERSION_INFO_DB_PATH),
        'T05': TableManager('t_T05', SOFTWARE_VERSION_INFO_DB_PATH)
    }
    print('开始向数据库写入path信息')
    for ver_type in ver_path_map:
        t_vers[ver_type].auto_commit = False
        for ver_id, ver_info in ver_path_map[ver_type].items():
            if ver_info['version'] == t_vers[ver_type].displayBriefData(ver_id, 'version')[0]:
                # print('Writing: %s -- %s' % (ver_info['version'], ver_info['path']))
                t_vers[ver_type].modifyLine(ver_id, path=ver_info['path'])
        t_vers[ver_type].commitData()
        t_vers[ver_type].auto_commit = True
    print('path信息写入数据库成功')
    return

