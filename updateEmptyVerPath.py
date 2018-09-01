from app.softpathmap import mapEmptyPathVersionsPath, writePathInfo


print('开始获取path为空的version')
ver_path_map = mapEmptyPathVersionsPath()
writePathInfo(ver_path_map)
