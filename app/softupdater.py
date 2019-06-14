import xlrd
import time
from app.pathinfo import *
from app.sqljob import TableManager


class Updater:
    def __init__(self, table_name, sheet_name):
        '''
            对数据库中的版本记录和xls文件中的版本记录，获取更新信息和更新数据库内容
            :param table_name: 数据库存放某个类型版本的表名
            :param sheet_name: xls文件中记录某个类型版本的sheet名
            * 2019.06.13: （New feature）设置两次更新检查最短间隔时间，避免高频率地检查
        '''
        self.table_name = table_name
        self.sheet_name = sheet_name
        self.version_xls_path = SOFTWARE_VERSION_INFO_XLS_PATH
        self.version_db_path = SOFTWARE_VERSION_INFO_DB_PATH
        self.vers_ready_to_update = None
        self.running_update = False
        self.CHECK_INTERVAL = 60
        self.last_update_info_check_time_mark = 0

    def getUpdateInfo(self):
        '''
            对比数据库与xls文件，获得需要更新的版本记录，以及数据库中过期的版本记录
            :returns 一次成功的更新返回的数据如下：
            {
                new: [ # 新增加的版本记录
                    (client, version, date, base, record, reason, remark, author),
                    (client, version, date, base, record, reason, remark, author),
                    ...
                ],
                expire: [ # 数据库上失效的版本记录
                    (client, version, date, base, record, reason, remark, author),
                    (client, version, date, base, record, reason, remark, author),
                    ...
                ]
            }
            失败的更新返回int数据
            0：  其他线程正在检测更新
            -1： 未找到xls文件或打开文件时失败
        '''
        if self.running_update:
            return 0
        if not os.path.isfile(self.version_xls_path):
            print('xls文件路径有误！！！')
            self.vers_ready_to_update = None
            return -1
        try:
            workbook = xlrd.open_workbook(self.version_xls_path)
            sheet = workbook.sheet_by_name(self.sheet_name)
        except (FileNotFoundError, xlrd.biffh.XLRDError) as e:
            print(e)
            self.vers_ready_to_update = None
            return -1

        if time.time() - self.last_update_info_check_time_mark <= self.CHECK_INTERVAL:
            # 短时间内避免重复检查IO
            if self.vers_ready_to_update is None:
                self.vers_ready_to_update = {'new': [], 'expire': []}
            return self.vers_ready_to_update
        t_soft = TableManager(self.table_name, self.version_db_path)
        ids = t_soft.getAllId()
        softs_existed = []
        for id in ids:
            vers_info = t_soft.displayBriefData(id, 'id', 'client', 'version', 'date', 'base', 'record', 'reason', 'remark', 'author')
            softs_existed.append(vers_info[1:])
        self.vers_ready_to_update = {'new': [], 'expire': []}

        for i in range(1, sheet.nrows):
            soft_info = tuple(sheet.row_values(i)[:8])
            if soft_info not in softs_existed:
                self.vers_ready_to_update['new'].append(soft_info)

            else:
                ver_idx = softs_existed.index(soft_info)
                softs_existed.pop(ver_idx)
        self.last_update_info_check_time_mark = time.time()
        self.vers_ready_to_update['expire'] = softs_existed
        return self.vers_ready_to_update

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
            if self.vers_ready_to_update is None:
                return False
            self.running_update = True
            try:
                t_soft = TableManager(self.table_name, self.version_db_path)
                t_soft.auto_commit = False
                for new_ver in self.vers_ready_to_update['new']:
                    t_soft.appendLine(client=new_ver[0],
                                      version=new_ver[1],
                                      date=new_ver[2],
                                      base=new_ver[3],
                                      record=new_ver[4],
                                      reason=new_ver[5],
                                      remark=new_ver[6],
                                      author=new_ver[7]),
                for expire_id in self.vers_ready_to_update['expire']:
                    t_soft.deleteLine(expire_id)
                t_soft.commitData()
                t_soft.auto_commit = True
                self.vers_ready_to_update = None
                return True
            except Exception as e:
                print(e)
                return False
            finally:
                self.running_update = False
