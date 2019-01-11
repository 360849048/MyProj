import time
import datetime
from app.pathinfo import *
from app.softpathmap import mapEmptyPathVersionsPath, writeAllPathInfo
from app.log import log


def updatePathInfoAutomatically():
    '''
        每天的22点到23点之间启动后台自动数据更新功能
    '''
    log.record('后台脚本程序启动')
    while True:
        now = datetime.datetime.now()
        if now.hour == 22:
            ver_path_map = mapEmptyPathVersionsPath()
            writeAllPathInfo(ver_path_map)
            info_to_record = '更新数据库path信息\n'
            for ver_type in ver_path_map:
                for ver_id, ver_info in ver_path_map[ver_type].items():
                    info_to_record += ver_info['version']
                    info_to_record += ': '
                    info_to_record += ver_info['path']
                    info_to_record += '\n'
            log.record(info_to_record)
            # 清理缓存目录
            try:
                if os.path.exists(CACHE_FILE_DIR):
                    for root, dirs, files in os.walk(CACHE_FILE_DIR):
                        for file in files:
                            os.remove(os.path.join(root, file))
                        for dir in dirs:
                            os.rmdir(os.path.join(root, dir))
            except:
                log.record('删除某些缓存文件失败...\n')
        time.sleep(3600)



