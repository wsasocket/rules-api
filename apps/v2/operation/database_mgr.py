import threading
import sqlite3
import os


class _DBManagerInterface(object):

    # 单例模式，管理用户的数据库操作，基础版本是sqlite3
    _instance_lock = threading.Lock()

    def __init__(self, *, file=None, url=None, port=None, user=None, password=None, dbname=None):
        self.connector = None
        self.cursor = None
        self._connect(file=file)

    def __del__(self):
        #  a finalizer or (improperly) a destructor
        self._close()

    def __new__(cls, *args, **kwargs):
        if not hasattr(_DBManagerInterface, "_instance"):
            with _DBManagerInterface._instance_lock:
                if not hasattr(_DBManagerInterface, "_instance"):
                    _DBManagerInterface._instance = object.__new__(cls)
        return _DBManagerInterface._instance

    def _connect(self, **connect_string):
        if not os.path.isfile(connect_string['file']):
            return
        try:
            self.connector = sqlite3.connect(connect_string['file'])
            self.cursor = self.connector.cursor()
        except sqlite3.Error as e:
            pass
            # print(e)

    def exec_sql(self, sql_string, *sql_values):
        # immutable queries,NOT accept single sql
        if self.cursor is None:
            return None
        commit = False if sql_string.split(' ')[0].upper().startswith('SELECT') else True
        try:
            res = self.cursor.execute(sql_string, sql_values)
            if commit:
                self.connector.commit()
            return res
        except sqlite3.Error as e:
            # print(e)
            return None

    # def exec_sql_many(self, sql_string, *sql_values):
    #     # immutable queries,NOT accept single sql
    #     try:
    #         return self.cursor.executemany(sql_string, sql_values)
    #     except sqlite3.Error as e:
    #         print(e)

    def _close(self):
        self.cursor.close()
        self.cursor = None
        self.connector.close()
        self.connector = None


class DBManager(_DBManagerInterface):
    """
    DBManager基本使用方法：
    初始化函数包括数据库连接功能，需要提供的参数需要使用关键字参数，包括
    file:sqlite3 的数据库文件
    url:远程数据库地址
    port:远程数据库端口
    user:远程数据库登录用户名
    password:远程数据库登录口令
    dbname:远程数据库名称
    连接后直接使用 exec_sql函数执行sql语句，返回值是数据集（如果有），出错就是None
    使用结束后 del db 删除实例，由于使用的是单例模式，建议在整体程序停止时再删除。
    函数说明：
    exec_sql(sql_string, *sql_values,*,commit=False)
    为了保证安全，使用不可变查询方式（immutable queries）！！！
    sql_string: sql语言结构，不包含数据，仅有数据占位符
    *sql_values: 可变长的数据，应当与占位符的数量及位置关系相匹配
    commit: 如果是插入或者更新操作，需要使用关键字化参数 commit=True
    """
    pass
