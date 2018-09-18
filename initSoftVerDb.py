'''
    初始化保存软件版本的数据库
    注意，运行这段脚本会删除原先的soft.db数据库，注意数据备份
'''
from app.rebuildSoftDb import rebuidSoftDb
from app.softpathmap import mapAllVersionsPath, writePathInfo
from app.softupdater import Updater
from app.pathinfo import *
from app.log import Log

if os.path.exists(CACHE_FILE_DIR):
    for root, dirs, files in os.walk(CACHE_FILE_DIR):
        for file in files:
            os.remove(os.path.join(CACHE_FILE_DIR, file))
        for dir in dirs:
            os.rmdir(os.path.join(CACHE_FILE_DIR, dir))
print('缓存文件清空完毕！')
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

if input('是否搜索源码路径？这可能需要很长时间 (y/n)') == 'y':
    ver_path_map = mapAllVersionsPath()
    writePathInfo(ver_path_map)
