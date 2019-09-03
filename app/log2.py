import sqlite3
import threading
from queue import Queue
import os
from app.pathinfo import *
from app.log import log as log_err


class Log:
    '''
        记录用户操作数据
        注意：用这个class创建对象，会自动创建另外一条线程，while死循环取队列中的log数据
    '''
    def __init__(self, log_file_path):
        self.path = log_file_path
        if not os.path.isfile(self.path):
            self.initLogFile()
        self.q = Queue()
        self.__thread_recoding = threading.Thread(target=self.__record, args=())
        self.__thread_recoding.start()

    def initLogFile(self):
        '''
        初始化日志文件，已存在就清空并重建
        :return:
        '''
        if os.path.isfile(self.path):
            os.remove(self.path)
        fp = open(self.path, 'w')
        fp.close()
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        sql = "CREATE TABLE t_log(id integer PRIMARY KEY AUTOINCREMENT, " \
              "time text NOT NULL DEFAULT (datetime('now', 'localtime')), username text NOT NULL," \
              "ip text NOT NULL, event text NOT NULL, description text NOT NULL)"
        c.execute(sql)
        conn.commit()
        conn.close()

    def record(self, ip, event, description='', username=''):
        self.q.put((ip, event, description, username))

    def __record(self):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        while True:
            try:
                ip, event, description, username = self.q.get()
                sql = "INSERT INTO t_log(username, ip, event, description) VALUES (%r, %r, %r, %r)" \
                      % (username, ip, event, description)
                c.execute(sql)
                conn.commit()
            except Exception as e:
                print(e)
                log_err.record(str(e))

    def readAll(self):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        sql = "SELECT * FROM t_log"
        c.execute(sql)
        return c.fetchall()


log = Log(LOG_DB_PATH)


if __name__ == '__main__':
    import time
    import random
    import math

    log = Log('./test_log.db')

    def record(username):
        while True:
            log.record('127.0.0.1', '插入数据', '', username)
            time.sleep(math.ceil(random.random()))

    threading._start_new_thread(record, ('adam', ))
    threading._start_new_thread(record, ('butty',))
