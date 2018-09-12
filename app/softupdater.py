import xlrd
from app.pathinfo import *
from app.sqljob import TableManager


class Updater:
    def __init__(self, table_name, sheet_name):
        self.table_name = table_name
        self.sheet_name = sheet_name
        self.version_xls_path = SOFTWARE_VERSION_INFO_XLS_PATH
        self.version_db_path = SOFTWARE_VERSION_INFO_DB_PATH
        self.vers_ready_to_append = None
        self.running_update = False

    def getUpdateInfo(self):
        '''
            对比数据库与xls文件，获得需要更新的软件版本
            对比逻辑：取各自(client, version, author)，若三者一致视为同版本，否则视为待添加的新版本
            注意table_name和sheet_name必须对应， 比如t_V05对应V05！
            :returns 成功打开xls文件并进行对比后，返回格式为
            [
                (client, version, date, base, record, reason, remark, author),
                (client, version, date, base, record, reason, remark, author),
                ...
            ]
            如果没有更新返回空list
            如果因为无法xls等失败则返回None
        '''
        if self.running_update:
            return 0
        if not os.path.isfile(self.version_xls_path):
            print('xls文件路径有误！！！')
            self.vers_ready_to_append = None
            return -1
        try:
            workbook = xlrd.open_workbook(self.version_xls_path)
            sheet = workbook.sheet_by_name(self.sheet_name)
        except (FileNotFoundError, xlrd.biffh.XLRDError) as e:
            print(e)
            self.vers_ready_to_append = None
            return -1
        t_soft = TableManager(self.table_name, self.version_db_path)
        ids = t_soft.getAllId()
        softs_existed = []
        for id in ids:
            # 3重验证，防止版本号重复的版本无法录入
            client, version, author = t_soft.displayBriefData(id, 'client', 'version', 'author')
            softs_existed.append((client, version, author))
        self.vers_ready_to_append = []
        for i in range(1, sheet.nrows):
            temp = sheet.row_values(i)
            client = temp[0]
            version = temp[1]
            author = temp[7]
            if version and (client, version, author) not in softs_existed:
                self.vers_ready_to_append.append(sheet.row_values(i)[:8])
        return self.vers_ready_to_append

    def startUpdate(self):
        '''
            将getUpdateInfo返回的数据，传入该函数，进行数据库写入更新操作
        '''
        if self.running_update:
            print('其他人正在更新')
            while self.running_update:
                # 等待其他线程操作完成
                pass
            return True
        else:
            if self.vers_ready_to_append is None:
                return False
            self.running_update = True
            try:
                t_soft = TableManager(self.table_name, self.version_db_path)
                for new_vers in self.vers_ready_to_append:
                    t_soft.appendLine(client=new_vers[0],
                                      version=new_vers[1],
                                      date=new_vers[2],
                                      base=new_vers[3],
                                      record=new_vers[4],
                                      reason=new_vers[5],
                                      remark=new_vers[6],
                                      author=new_vers[7],
                                      path='')
                self.vers_ready_to_append = None
                return True
            except:
                return False
            finally:
                self.running_update = False
