import time
import datetime
from app.softpathmap import mapEmptyPathVersionsPath, writePathInfo
from app.log import log


def updatePathInfoAutomatically():
    '''
        每天的22点到23点之间启动后台自动数据更新功能
    '''
    while True:
        now = datetime.datetime.now()
        if now.hour == 22:
            ver_path_map = mapEmptyPathVersionsPath()
            writePathInfo(ver_path_map)
            info_to_record = '更新数据库path信息：\n'
            for ver_type in ver_path_map:
                for ver_id, ver_info in ver_path_map[ver_type].items():
                    info_to_record += ver_info['version']
                    info_to_record += ': '
                    info_to_record += ver_info['path']
                    info_to_record += '\n'
            log.record(info_to_record)
        time.sleep(3600)



