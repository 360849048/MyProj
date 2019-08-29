import os


'''
Python调用的路径
   对于python运行环境来说，此时工作路径为  /MyProj
'''
# 存放IO信息的数据库路径
IO_INFO_DB_PATH = './app/libfiles/data.db'
# 标准文件目录
STD_LIB_FILE_DIR = './app/libfiles/'
STD_MODULE_LIB_XLSX = os.path.join(STD_LIB_FILE_DIR, '常用硬件表.xlsx')
# 标准配置文件目录
STD_HK_FILE_DIR = os.path.join(STD_LIB_FILE_DIR, '配置文件/硬件配置文件')
STD_FCF_FILE_DIR = os.path.join(STD_LIB_FILE_DIR, '配置文件/功能配置文件')
STD_SYS_FILE_DIR = os.path.join(STD_LIB_FILE_DIR, '配置文件/系统文件')
NOR_SAFETY_RELAY_FILE_DIR = os.path.join(STD_LIB_FILE_DIR, '配置文件/安全继电器文件/Normal')
E73_SAFETY_RELAY_FILE_DIR = os.path.join(STD_LIB_FILE_DIR, '配置文件/安全继电器文件/E73')
# 生成的目标文件缓存目录
CACHE_FILE_DIR = './app/static/cache/'
# 日志数据路径
LOG_DB_PATH = './app/libfiles/log.db'
# 用户信息数据数据库信息
USER_INFO_DB_PATH = './app/libfiles/user.db'
ACCOUNT_TABLE_NAME = 't_user'

'''
Flask框架调用的路径
   对于Flask框架来说，此时工作路径为  /app   且所有HTTP请求的文件必须位于 /app/static目录之下
'''
# 网页入口文件路径
ENTRY_HTML_PATH = './static/index.html'
# 生成的目标文件缓存目录
URL_DIR = './static/cache/'

# 存放软件版本的数据库路径
SOFTWARE_VERSION_INFO_DB_PATH = './app/libfiles/soft.db'

# 存放软件版本的xls文件路径（！注意服务器上该文件的路径）
SOFTWARE_VERSION_INFO_XLS_PATH = 'Y:/软件版本登记/软件版本登记表.xls'
if not os.path.isfile(SOFTWARE_VERSION_INFO_XLS_PATH):
    # 如果部署与服务器上，该xls文件的正确路径应该如下
    SOFTWARE_VERSION_INFO_XLS_PATH = 'G:/软件版本登记/软件版本登记表.xls'


if not os.path.isdir(CACHE_FILE_DIR):
    os.mkdir(CACHE_FILE_DIR)


# 存放软件源文件的目录
SOFTWARE_SRC_CODE_DIR = 'E:/工作重要备份/'
if not os.path.isdir(SOFTWARE_SRC_CODE_DIR):
    # 如果部署在服务器上，搜索路径更改为G盘根目录
    SOFTWARE_SRC_CODE_DIR = 'G:/'
