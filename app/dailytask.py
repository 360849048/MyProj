import time
import datetime
import shutil
from app.pathinfo import *
from app.softpathmap import mapEmptyPathVersionsPath, writeAllPathInfo, mapAllVersionsPath
from app.log import log
from app.softrefresh import handleRefresh


def updatePathInfoAutomatically():
    '''
        每天固定时间段内启动后台自动数据更新功能
        * 2019.06.14: （Bug fix）在同一个os.walk循环下无法同时删除文件和文件夹
        * 2019.06.20: （New Feature）每周固定时间重置软件版本库的路径信息
    '''
    log.record('后台脚本程序启动')
    while True:
        now = datetime.datetime.now()
        if now.hour == 1:
            # 首先清理缓存目录
            try:
                shutil.rmtree(CACHE_FILE_DIR)
                os.mkdir(CACHE_FILE_DIR)
            except:
                log.record('删除某些缓存文件失败...\n')
            if now.weekday() != 6:
                # 非周日仅搜索标记的版本和路径为空的版本
                # 将今天用户标记路径有误的版本进行path字段清空，这样后续就会对该版本路径进行重新搜索
                handle_num = handleRefresh()
                log.record('处理了路径标记版本，数量: ' + str(handle_num))
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
            else:
                # 将版本库中所有的路径信息更新
                ver_path_map = mapAllVersionsPath()
                writeAllPathInfo(ver_path_map)
                log.record('重建软件版本路径关系')
        time.sleep(3600)



