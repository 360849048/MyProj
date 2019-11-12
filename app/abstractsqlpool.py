import sqlite3


'''
本模块定义了数据库连接池的操作方法
'''


class AbstractConnPool:
    instance = None
    initialized = False
    # 数据库的位置
    db_path = ""
    # 初始化的连接数量
    MIN_CONN = 3
    # 连接池内最大空闲连接数
    MAX_CONN = 5

    def __new__(cls):
        cls.instance = super().__new__(cls) if cls.instance is None else cls.instance
        return cls.instance

    def __init__(self):
        if self.initialized:
            return
        self.initialized = True

        # conn_pool: 连接池内的空闲连接
        self.conn_pool = []
        # cur_conn_num: 空闲连接数 + 被占用的连接数
        self.cur_conn_num = self.MIN_CONN
        for i in range(self.MIN_CONN):
            # 如果不使用 check_same_thread=False，会报错
            self.conn_pool.append(sqlite3.connect(self.db_path, check_same_thread=False))

    def __del__(self):
        print(self.conn_pool)
        for conn in self.conn_pool:
            conn.close()

    def get(self):
        if len(self.conn_pool) == 0:
            self.cur_conn_num += 1
            return sqlite3.connect(self.db_path, check_same_thread=False)
        return self.conn_pool.pop()

    def giveBack(self, conn):
        if not isinstance(conn, sqlite3.Connection):
            pass
        elif len(self.conn_pool) > self.MAX_CONN:
            # 连接池的空闲连接数已经达到MAX_CONN，丢弃归还的连接
            conn.close()
            self.cur_conn_num -= 1
        else:
            self.conn_pool.append(conn)


