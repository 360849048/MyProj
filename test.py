import time
from app.softrefresh import *
from app.pathinfo import *
from app.sqljob import DbManager



db_soft = DbManager(SOFTWARE_VERSION_INFO_DB_PATH)
db_soft.addTableColumns('t_V05', 'torefresh')
for table_name in db_soft.getAllTables():
    if table_name == 'sqlite_sequence':
        continue
    db_soft.addTableColumns(table_name, 'torefresh')

print(db_soft.getTableColumns('t_V05'))
print(db_soft.getTableColumns('sqlite_sequence'))
print(db_soft.getAllTables())
#
t_vers = {
        'V01': TableManager('t_V01', SOFTWARE_VERSION_INFO_DB_PATH),
        'V02': TableManager('t_V02', SOFTWARE_VERSION_INFO_DB_PATH),
        'V03V04': TableManager('t_V03V04', SOFTWARE_VERSION_INFO_DB_PATH),
        'V05': TableManager('t_V05', SOFTWARE_VERSION_INFO_DB_PATH),
        'T05': TableManager('t_T05', SOFTWARE_VERSION_INFO_DB_PATH)
    }
print('start mark every')
time_mark = time.time()
markToRefresh('t_V05', t_vers['V05'].getAllId())
print('mark耗时: ' + str(time.time() - time_mark))

print('start handle refresh')
time_mark = time.time()
handleRefresh()
print('handle耗时: ' + str(time.time() - time_mark))

for id in t_vers['V05'].getAllId():
    print(t_vers['V05'].displayDetailedData(id))

