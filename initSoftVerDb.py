'''
    初始化保存软件版本的数据库
    注意，运行这段脚本会删除原先的soft.db数据库，注意数据备份
'''
import datetime
import shutil
from app.rebuildSoftDb import rebuidSoftDb
from app.softpathmap import mapAllVersionsPath, writePathInfo
from app.softupdater import Updater
from app.pathinfo import *
from app.log import log

if os.path.exists(CACHE_FILE_DIR):
    for root, dirs, files in os.walk(CACHE_FILE_DIR):
        for file in files:
            os.remove(os.path.join(CACHE_FILE_DIR, file))
        for dir in dirs:
            os.rmdir(os.path.join(CACHE_FILE_DIR, dir))
print('缓存文件清空完毕！')
# 提前备份一个soft.db文件，万一写烂给留条后路撤退
now = datetime.datetime.now()
db_cpy_name = 'soft_cpy' + now.strftime('%Y%m%d%H%M%S') + '.db'
db_cpy_path = os.path.join(os.path.dirname(SOFTWARE_VERSION_INFO_DB_PATH), db_cpy_name)
shutil.copyfile(SOFTWARE_VERSION_INFO_DB_PATH, db_cpy_path)
if input('是否重建数据库？这会清空原先数据库 (y/n)') == 'y':
    print('开始重建数据')
    rebuidSoftDb()
    print('开始导入数据到数据库...')
    updaters = {
        'V01': Updater('t_V01', 'V01'),
        'V02': Updater('t_V02', 'V02'),
        'V03V04': Updater('t_V03V04', 'V03&V04'),
        'V05': Updater('t_V05', 'V05'),
        'T05': Updater('t_T05', 'T05'),
    }
    for ver_type, updater in updaters.items():
        print('获取', ver_type, '待更新数据...')
        updater.getUpdateInfo()
        print('写入', ver_type, '数据...')
        updater.startUpdate()
    print('完成数据导入')
    log.record('重建软件版本数据库')

if input('是否搜索源码路径？这可能需要很长时间 (y/n)') == 'y':
    ver_path_map = mapAllVersionsPath()
    writePathInfo(ver_path_map)
    log.record('重建软件版本路径关系')
