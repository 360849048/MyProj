import os


'''
Python调用的路径
   对于python运行环境来说，此时工作路径为  /MyProj
'''
# 存放IO信息的数据库路径
IO_INFO_DB_PATH = './app/libfiles/data.db'
# 标准文件目录
STD_LIB_FILE_DIR = './app/libfiles/'
# 标准配置文件目录
STD_HK_FILE_DIR = os.path.join(STD_LIB_FILE_DIR, '配置文件/硬件配置文件')
STD_FCF_FILE_DIR = os.path.join(STD_LIB_FILE_DIR, '配置文件/功能配置文件')
STD_SYS_FILE_DIR = os.path.join(STD_LIB_FILE_DIR, '配置文件/系统文件')
NOR_SAFETY_RELAY_FILE_DIR = os.path.join(STD_LIB_FILE_DIR, '配置文件/安全继电器文件/Normal')
E73_SAFETY_RELAY_FILE_DIR = os.path.join(STD_LIB_FILE_DIR, '配置文件/安全继电器文件/E73')
# 生成的目标文件缓存目录
CACHE_FILE_DIR = './app/static/cache/'


'''
Flask框架调用的路径
   对于Flask框架来说，此时工作路径为  /app   且所有HTTP请求的文件必须位于 /app/static目录之下
'''
# 网页入口文件路径
ENTRY_HTML_PATH = './static/index.html'
# 生成的目标文件缓存目录
URL_DIR = './static/cache/'
