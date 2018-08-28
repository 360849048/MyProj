import xlrd
from app.pathinfo import *
from app.sqljob import TableManager


def update(table_name, sheet_name):
    if not os.path.isfile(SOFTWARE_VERSION_INFO_XLS_PATH):
        return None
    try:
        workbook = xlrd.open_workbook(SOFTWARE_VERSION_INFO_XLS_PATH)
        sheet = workbook.sheet_by_name(sheet_name)
    except (FileNotFoundError, xlrd.biffh.XLRDError) as e:
        print(e)
        return None
    print('更新软件版本库...')
    t_soft = TableManager(table_name, SOFTWARE_VERSION_INFO_DB_PATH)
    ids = t_soft.getAllId()
    softs_existed = []
    for id in ids:
        # 3重验证，防止版本号重复的版本无法录入
        client, version, author = t_soft.displayBriefData(id, 'client', 'version', 'author')
        softs_existed.append((client, version, author))
    softs_ready_to_append = []
    print('即将更新的版本为：')
    for i in range(1, sheet.nrows):
        temp = sheet.row_values(i)
        client = temp[0]
        version = temp[1]
        author = temp[7]
        if version and (client, version, author) not in softs_existed:
            softs_ready_to_append.append(sheet.row_values(i)[:8])
            print(version)
    for new_soft in softs_ready_to_append:
        t_soft.appendLine(client=new_soft[0],
                          version=new_soft[1],
                          date=new_soft[2],
                          base=new_soft[3],
                          record=new_soft[4],
                          reason=new_soft[5],
                          remark=new_soft[6],
                          author=new_soft[7])
    if len(softs_ready_to_append) == 0:
        print('没有任何更新！')
    else:
        print('更新完毕！')
    return tuple(softs_ready_to_append)

