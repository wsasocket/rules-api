import threading
import sqlite3
import os


class _DBManagerInterface(object):
    """
    
    """
    # 单例模式，管理用户的数据库操作，基础版本是sqlite3
    _instance_lock = threading.Lock()

    def __init__(self):
        self.connector = None
        self.cursor = None

    def __del__(self):
        #  a finalizer or (improperly) a destructor
        self._close()
        super().__del__()

    def __new__(cls, *args, **kwargs):
        if not hasattr(_DBManagerInterface, "_instance"):
            with _DBManagerInterface._instance_lock:
                if not hasattr(_DBManagerInterface, "_instance"):
                    _DBManagerInterface._instance = object.__new__(cls)
        return _DBManagerInterface._instance

    def connect(self, connect_string):
        if not os.path.isfile(connect_string):
            return
        try:
            self.connector = sqlite3.connect(connect_string)
            self.cursor = self.connector.cursor()
        except sqlite3.Error as e:
            print(e)

    def exec_sql(self, sql_string, *sql_values):
        # immutable queries,NOT accept single sql
        if self.cursor is None:
            return None
        try:
            return self.cursor.execute(sql_string, sql_values)
        except sqlite3.Error as e:
            print(e)

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
    pass
