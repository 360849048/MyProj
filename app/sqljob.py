import sqlite3
import os

# #
# 本模块用来对路径为 "path_db" 数据库进行简单操作，一般步骤如下
# 1. 实例化DbManger，查看该数据库包含的所有表。可对数据库进行：
#       查看已有表，表的列； 新建表，重命名表，备份表，删除列。
# 2. 实例化TableManger，可对表进行：
#       查看列，查看行和id，显示并返回行，行的查找； 插入新行，删除行，修改行。
#  注意：所有表内部数据以隐藏的列 "id" 进行传递，id列会自动生成。
# #

__Author__ = "J"



class DbManager:
    def __init__(self, path_db):
        self.conn = sqlite3.connect(path_db)
        self.c = self.conn.cursor()
        self.__tables = self.getAllTables()

    def __del__(self):
        try:
            self.c.close()
            self.conn.close()
            print("The database closed.")
        except:
            print("关闭数据库异常!!!")

    def createNewTable(self, table_name, columns):
        # columns是一个tuple或者list数据
        if table_name not in self.__tables:
            sql = "CREATE TABLE IF NOT EXISTS %s(id integer PRIMARY KEY AUTOINCREMENT" % table_name + (",%s text"*len(columns)) % columns + ")"
            self.c.execute(sql)
            self.__tables = self.getAllTables()
        else:
            print("The table %r has already existed!" % table_name)

    def dropTable(self, table_name):
        if table_name in self.__tables:
            sql = "DROP TABLE IF EXISTS %s" % table_name
            self.c.execute(sql)
            self.__tables = self.getAllTables()
        else:
            print("There is no table named %r" % table_name)

    def renameTable(self, old_table_name, new_table_name):
        if old_table_name in self.__tables and new_table_name not in self.__tables:
            sql = "ALTER TABLE %s RENAME TO %s" % (old_table_name, new_table_name)
            self.c.execute(sql)
            self.conn.commit()
        elif old_table_name not in self.__tables:
            print("There is no table named %r", old_table_name)
        else:
            print("The new name %r has already existed in this database" % new_table_name)

    def backupTable(self, original_table_name, new_table_name=None):
        # 将表复制到同一个数据库，每行的id不会发生变化
        if original_table_name in self.__tables:
            if new_table_name == None:
                new_table_name = original_table_name + "_backup"
            while new_table_name in self.__tables:
                new_table_name = new_table_name + "_副本"
            print(new_table_name)

            columns = self.getTableColumns(original_table_name)
            sql1 = "CREATE TABLE IF NOT EXISTS %s(id integer PRIMARY KEY AUTOINCREMENT" % new_table_name + (",%s text"*len(columns)) % columns + ")"
            sql2 = "INSERT INTO %s" % new_table_name + " SELECT * FROM %s" % original_table_name
            self.c.execute(sql1)
            self.c.execute(sql2)
            self.conn.commit()
        else:
            print("There is no table named %s", original_table_name)

    def copyTableToOtherDb(self, table_name, path_other_database, Reorder=False):
        # Reorder为True，将表重新整理，移除空余的id，并复制到新的数据库中。例如原表有id为(1, 2, 4)，新的表中id为(1, 2, 3)
        table_names = []
        other_db_conn = sqlite3.connect(path_other_database)
        other_db_cursor = other_db_conn.cursor()
        other_db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        temp = other_db_cursor.fetchall()
        for table in temp:
            table_names.append(table[0])
        if table_name in table_names:
            print("A table named %s has already exsited in database %s" % (table_name, os.path.basename(path_other_database)))
            return table_name
        columns = self.getTableColumns(table_name)
        self.c.execute("SELECT * FROM %s" % table_name)
        datas = self.c.fetchall()
        sql1 = "CREATE TABLE IF NOT EXISTS %s(id integer PRIMARY KEY AUTOINCREMENT" % table_name + (",%s text" * len(columns)) % columns + ")"
        other_db_cursor.execute(sql1)
        for data in datas:
            if Reorder:
                sql2 = "INSERT INTO %s(" % table_name + (((",%s"*len(columns)).strip(',')) % columns) + ") VALUES(" + (",?"*len(columns)).strip(',') + ")"
                other_db_cursor.execute(sql2, tuple(data[1:]))
            else:
                sql2 = "INSERT INTO %s " % table_name + "VALUES(" + (",?"*len(data)).strip(',') + ")"
                other_db_cursor.execute(sql2, tuple(data))
        other_db_conn.commit()
        return table_name

    def deleteTableColumns(self, table_name, *columns_to_del, Reorder=False):
        # Reorder为True，将表重新整理，移除空余的id，。例如原表有id为(1, 2, 4)，新的表中id为(1, 2, 3)
        columns_original = list(self.getTableColumns(table_name))
        temp_table = "temp_table"
        for column in columns_to_del:
            if column not in columns_original:
                print("Columns need to be deleted are not in table %s, the table is not modified!" % table_name)
                return
            else:
                columns_original.pop(columns_original.index(column))
        new_columns = tuple(columns_original)
        sql1 = "CREATE TABLE IF NOT EXISTS %s(id integer PRIMARY KEY AUTOINCREMENT" % temp_table + (",%s text" * len(new_columns)) % new_columns + ")"
        if Reorder:
            sql2 = "INSERT INTO %s(" % temp_table + ((",%s"*len(new_columns)) % new_columns).strip(",") + ")" + " SELECT " + ((",%s"*len(new_columns)) % new_columns).strip(",") + " FROM %s" % table_name
        else:
            sql2 = "INSERT INTO %s" % temp_table + " SELECT id" + (",%s"*len(new_columns)) % new_columns + " FROM %s" % table_name
        self.c.execute(sql1)
        self.c.execute(sql2)
        self.conn.commit()
        self.dropTable(table_name)
        self.renameTable(temp_table, table_name)

    def addTableColumns(self, table_name, *columns_to_add):
        columns_original = self.getTableColumns(table_name)
        for column in columns_to_add:
            if column in columns_original:
                print("Columns need to be add have already existed in table %s, the table is not modified!" % table_name)
                return
        for column in columns_to_add:
            self.c.execute("ALTER TABLE %s ADD COLUMN %s text" % (table_name, column))
        self.conn.commit()

    def renameTableColumns(self, table_name, **columns_to_rename):
        columns_original = list(self.getTableColumns(table_name))
        for k, v in columns_to_rename.items():
            if k not in columns_original:
                print("Columns need to be renamed are not in table %s, the table is not modified!" % table_name)
                return
            else:
                columns_original[columns_original.index(k)] = v
        new_columns = tuple(columns_original)
        temp_table = "temp_table"
        sql1 = "CREATE TABLE IF NOT EXISTS %s(id integer PRIMARY KEY AUTOINCREMENT" % temp_table + (",%s text" * len(new_columns)) % new_columns + ")"
        sql2 = "INSERT INTO %s" % temp_table + " SELECT * FROM %s" % table_name
        self.c.execute(sql1)
        self.c.execute(sql2)
        self.c.execute("DROP TABLE IF EXISTS %s" % table_name)
        self.c.execute("ALTER TABLE %s RENAME TO %s" % (temp_table, table_name))
        self.conn.commit()

    # ###################### 以下所有为查询数据相关函数 ######################
    def getAllTables(self):
        table_names = []
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        temp = self.c.fetchall()
        for table in temp:
            table_names.append(table[0])
        table_names = tuple(table_names)
        return table_names

    def getTableColumns(self, table_name):
        # 获取表中列的名字
        self.c.execute("PRAGMA table_info(%s)" % table_name)
        temp = self.c.fetchall()
        columns = []
        for i in temp:
            columns.append(i[1])
        columns = tuple(columns)
        return columns[1:]

    def execSQL(self, sql):
        self.c.execute(sql)
        return self.c.fetchall()

class TableManager:
    def __init__(self, table_name, path_db, columns4init=('如果不是创建新表，不需要填写该参数',)):
        # 修改表内容后自动保存
        self.auto_commit = True
        self.table = table_name
        self.columns = columns4init

        self.conn = sqlite3.connect(path_db)
        self.c = self.conn.cursor()
        sql = ("CREATE TABLE IF NOT EXISTS %s(id integer PRIMARY KEY AUTOINCREMENT" + ",%s text" * len(self.columns) + ")") % ((self.table,) + self.columns)
        self.c.execute(sql)
        self.columns = self._getColumns()

    def __del__(self):
        try:
            self.c.close()
            self.conn.close()
        except:
            print("Fatal Error: The database: %s can't be closed!!!" % self.table)

    def appendLine(self, **columns):
        # 表末尾添加一条新行
        col = []
        val = []
        for k, v in columns.items():
            col.append(k)
            val.append(v)
        sql = "INSERT INTO %s(" % self.table + ((",%s" * len(col)) % tuple(col)).strip(',') + ") VALUES(" + (",?" * len(col)).strip(',') + ")"
        self.c.execute(sql, tuple(val))
        if self.auto_commit:
            self.conn.commit()

    def deleteLine(self, id):
        # 删除id对应的某一行
        self.c.execute("DELETE FROM %s WHERE id=?" % self.table, (str(id),))
        if self.auto_commit:
            self.conn.commit()

    def _deleteLines(self, ids):
        # 删除tuple内所有id对应的行
        for id in ids:
            self.c.execute("DELETE FROM %s WHERE id=?" % self.table, (str(id),))
        if self.auto_commit:
            self.conn.commit()

    def modifyLine(self, id, **columns):
        for k, v in columns.items():
            self.c.execute("UPDATE %s SET %s=? WHERE id=?" % (self.table, str(k)), (str(v), str(id)))
        if self.auto_commit:
            self.conn.commit()

    def commitData(self):
        # 手动提交数据
        self.conn.commit()

    def rollbackData(self):
        # 手动回滚数据操作
        self.conn.rollback()

    #  ###################### 以下所有为查询数据相关函数 ######################

    def _getColumns(self):
        # 获取表中列的名字
        self.c.execute("PRAGMA table_info(%s)" % self.table)
        temp = self.c.fetchall()
        columns = []
        for i in temp:
            columns.append(i[1])
        columns = tuple(columns)
        return columns[1:]

    def getColumns(self):
        return self.columns

    def countLines(self):
        sql = "SELECT count(*) FROM %s" % self.table
        self.c.execute(sql)
        result = self.c.fetchone()
        return result[0]

    def getAllId(self, orderby=None, desc=False):
        # 返回所有行id，例如(1, 2, 3, 4, ...)
        # 按column对所有id进行升序排列，当desc为True时，降序排列
        ids = []
        if orderby is None or orderby not in self.columns:
            sql = 'SELECT id FROM %s' % self.table
        else:
            if desc:
                sql = 'SELECT id FROM %s ORDER BY %s DESC' % (self.table, orderby)
            else:
                sql = 'SELECT id FROM %s ORDER BY %s' % (self.table, orderby)
        self.c.execute(sql)
        result = self.c.fetchall()
        for i in result:
            ids.append(i[0])
        ids = tuple(ids)
        return ids

    def displayBriefData(self, id, *columns):
        if len(columns) == 0:
            columns = (self.columns[0],)
        sql = "SELECT " + (("%s,"*len(columns)) % columns).strip(',') + " FROM %s WHERE id=?" % self.table
        self.c.execute(sql, (str(id),))
        line = self.c.fetchone()
        return line

    def displayBriefDatas(self, ids, *columns):
        lines = []
        for id in ids:
            lines.append(self.displayBriefData(id, *columns))
        lines = tuple(lines)
        return lines

    def displayDetailedData(self, id):
        # if id not in self.getAllId():
        #     return None
        self.c.execute("SELECT * FROM %s WHERE id=?" % self.table, (str(id), ))
        line = self.c.fetchone()
        if not line:
            return None
        # return line[1:]
        temp_cols = list(self.columns)
        temp_cols.insert(0, "id")
        return dict(zip(temp_cols, line))

    def searchDataByKey(self, **column):
        # 模糊匹配，返回id，例如参数为title="bug"，结果返回(1, 2, 3,...)
        ids = []
        key = []
        var = []
        mix = []
        if len(column) == 0:
            print("没有进行匹配，请输入至少1个列名及对应关键字")
            return ()
        for k, v in column.items():
            key.append(str(k))
            var.append(str(v))
            mix.append('%'+str(v)+'%')
        # 把key中的每项依次间隔插入到mix中，比如[1,3,5]插入到[2,4,6]后得到[1,2,3,4,5,6]
        for n in range(len(key)):
            mix.insert(n*2, key[n])
        sql = "SELECT id FROM %s WHERE " % self.table + "%s LIKE %r" % tuple(mix[:2]) + " AND %s LIKE %r" * (len(key) - 1) % tuple(mix[2:])
        self.c.execute(sql)
        result = self.c.fetchall()
        for item in result:
            ids.append(item[0])
        ids = tuple(ids)
        return ids

    def searchDataInTable(self, keyword, *exclude):
        ids = set()
        target_cols = tuple(col for col in self.columns if col not in exclude)
        for col in target_cols:
            sql = 'SELECT id FROM %s WHERE ' % self.table + "%s LIKE %r" % (col, '%'+keyword + '%')
            self.c.execute(sql)
            result = self.c.fetchall()
            for item in result:
                ids.add(item[0])
        return tuple(ids)


if __name__ == '__main__':
    import re
    import time


    # 多表模糊匹配查询速度测试
    time_mark = time.time()
    t_vers = {
        'V01': TableManager('t_V01', './libfiles/soft.db'),
        'V02': TableManager('t_V02', './libfiles/soft.db'),
        'V03V04': TableManager('t_V03V04', './libfiles/soft.db'),
        'V05': TableManager('t_V05', './libfiles/soft.db'),
        'T05': TableManager('t_T05', './libfiles/soft.db')
    }

    string = '华 麦 邵 阀门'
    ret_data = {'itemsNum': 0, 'items': {}}
    keywords = re.split(r'\s+', string)
    key = 0
    for soft_type in t_vers:
        ids_for_each_keys = []

        for keyword in keywords:
            ids_for_each_keys.append(t_vers[soft_type].searchDataInTable(keyword, 'path'))
        ids = ids_for_each_keys[0]
        for i in range(1, len(ids_for_each_keys)):
            ids = tuple(id for id in ids if id in ids_for_each_keys[i])
        ret_data['itemsNum'] += len(ids)
        for soft_id in ids:
            ret_data['items'][key] = t_vers[soft_type].displayDetailedData(soft_id)
            key += 1
    print(ret_data)
    print('一共耗时: ', time.time() - time_mark)

    for i in range(5):
        ids = t_vers['V05'].searchDataByKey(client='印度',date='2018.08.30',reason='合同',author='应志峰',record='1.吹气功能特殊',version='V05_39_51', base='V05_39_50')
        print(ids)
