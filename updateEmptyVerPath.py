from app.softpathmap import mapEmptyPathVersionsPath, writeAllPathInfo
from app.log import log


print('开始获取path为空的version')
ver_path_map = mapEmptyPathVersionsPath()
writeAllPathInfo(ver_path_map)
info_to_record = '更新数据库path信息：\n'
for ver_type in ver_path_map:
    for ver_id, ver_info in ver_path_map[ver_type].items():
        info_to_record += ver_info['version']
        info_to_record += ': '
        info_to_record += ver_info['path']
        info_to_record += '\n'
log.record(info_to_record)
