'''
该模块用来处理soft.db各表中torefresh字段，包括：
    * 根据表名和行id，对数据进行torefresh字段的标记，写1
    * 对数据库内所有表的内容进行搜索，对torefresh字段被写1的数据行的path字段清空
'''
from app.sqljob import TableManager
from app.pathinfo import *


def markToRefresh(table_name, ids):
    t_soft = TableManager(table_name, SOFTWARE_VERSION_INFO_DB_PATH)
    if isinstance(ids, int):
        t_soft.modifyLine(ids, torefresh='1')
    elif isinstance(ids, tuple) or isinstance(ids, list) or isinstance(ids, set):
        # 多次commit很耗费性能，需要避免
        t_soft.auto_commit = False
        for id in ids:
            t_soft.modifyLine(id, torefresh='1')
        t_soft.commitData()
        t_soft.auto_commit = True


def handleRefresh():
    '''
    对数据库内所有表的内容进行搜索，对torefresh字段被写1的数据行的path字段清空
    :return:   处理的版本数量
    '''
    count = 0
    t_vers = {
        'V01': TableManager('t_V01', SOFTWARE_VERSION_INFO_DB_PATH),
        'V02': TableManager('t_V02', SOFTWARE_VERSION_INFO_DB_PATH),
        'V03V04': TableManager('t_V03V04', SOFTWARE_VERSION_INFO_DB_PATH),
        'V05': TableManager('t_V05', SOFTWARE_VERSION_INFO_DB_PATH),
        'T05': TableManager('t_T05', SOFTWARE_VERSION_INFO_DB_PATH)
    }
    for soft_type in t_vers:
        ids = t_vers[soft_type].searchDataByKey(torefresh='1')
        t_vers[soft_type].auto_commit = False
        for id in ids:
            t_vers[soft_type].modifyLine(id, path='', torefresh='')
            count += 1
        t_vers[soft_type].commitData()
        t_vers[soft_type].auto_commit = True
    return count
