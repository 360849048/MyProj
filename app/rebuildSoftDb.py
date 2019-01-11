'''
    初始化soft.db数据库（如果已存在则清空数据库重建）
'''
from app.sqljob import *
from app.pathinfo import *

def rebuidSoftDb():
    db = DbManager(SOFTWARE_VERSION_INFO_DB_PATH)
    # 如已存在删除原先的表
    db.dropTable('t_V01')
    db.dropTable('t_V02')
    db.dropTable('t_V03V04')
    db.dropTable('t_V05')
    db.dropTable('t_T05')
    # 新建各个表
    db.createNewTable('t_V01', ('client', 'version', 'date', 'base', 'record', 'reason', 'remark', 'author', 'path', 'torefresh'))
    db.createNewTable('t_V02', ('client', 'version', 'date', 'base', 'record', 'reason', 'remark', 'author', 'path', 'torefresh'))
    db.createNewTable('t_V03V04', ('client', 'version', 'date', 'base', 'record', 'reason', 'remark', 'author', 'path', 'torefresh'))
    db.createNewTable('t_V05', ('client', 'version', 'date', 'base', 'record', 'reason', 'remark', 'author', 'path', 'torefresh'))
    db.createNewTable('t_T05', ('client', 'version', 'date', 'base', 'record', 'reason', 'remark', 'author', 'path', 'torefresh'))
    print('ok')
