import unittest
from apps.v2.operation.database_mgr import DBManager
import os
import sqlite3


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.path.isfile('test.db'):
            os.remove('test.db')
        connector = sqlite3.connect("test.db")
        cursor = connector.cursor()
        sql1 = 'CREATE TABLE USER (ID INTEGER PRIMARY KEY AUTOINCREMENT ,NAME TEXT NOT NULL,PASSWORD TEXT NOT NULL);'
        val1 = []
        sql2 = "INSERT INTO USER(NAME,PASSWORD) VALUES(:1,:2);"
        val2 = ['admin', '/F4DjTilcDIIVEHn/nAQsA==']
        sql3 = sql2
        val3 = ['root', '/OqSD3QStdp74M9CuMk3WQ==']
        cursor.execute(sql1, val1)
        connector.commit()
        cursor.execute(sql2, val2)
        cursor.execute(sql3, val3)
        connector.commit()
        cursor.close()
        connector.close()
        print(DBManager.__doc__)

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove('test.db')
        except FileNotFoundError as e:
            # print(e)
            pass
        except PermissionError as e:
            # print(e)
            pass

    def test_exec_sql_select(self):
        # 查询
        db = DBManager(file='test.db')
        v = db.exec_sql('select * from user where name=:1', 'admin')
        count = 0
        # print('test_exec_sql_select')
        for i in v:
            # print(i)
            count += 1
        self.assertIsInstance(v, sqlite3.Cursor)
        self.assertTrue(count == 1)
        del db

    def test_exec_sql_insert(self):
        # 增加
        db = DBManager(file='test.db')
        v = db.exec_sql('INSERT INTO USER(name,password) values(:1,:2)', 'james', 'XXXXXXXX')
        self.assertEqual(type(v), sqlite3.Cursor)
        v = db.exec_sql('select * from user where name=:1', 'james')
        self.assertEqual(type(v), sqlite3.Cursor)
        # print('test_exec_sql_insert')
        count = 0
        for i in v:
            # print(i)
            count += 1
        self.assertTrue(count == 1)
        del db

    def test_exec_sql_update(self):
        # 修改
        db = DBManager(file='test.db')
        v = db.exec_sql('INSERT INTO USER(name,password) values(:1,:2)', 'Ryan', 'ZZZZZZ')
        self.assertEqual(type(v), sqlite3.Cursor)
        v = db.exec_sql('UPDATE USER SET NAME=:1 where name=:2', 'Bob', 'Ryan')
        self.assertEqual(type(v), sqlite3.Cursor)
        v = db.exec_sql('select * from user where name=:1', 'Bob')
        # print('test_exec_sql_update')
        count = 0
        for i in v:
            # print(i)
            count += 1
        self.assertTrue(count == 1)
        del db

    def test_exec_sql_delete(self):
        # 删除记录
        db = DBManager(file='test.db')
        v = db.exec_sql('INSERT INTO USER(name,password) values(:1,:2)', 'james', 'XXXXXXXX')
        self.assertTrue(v.rowcount, 1)
        v = db.exec_sql('DELETE FROM USER where name=:1', 'james')
        self.assertEqual(type(v), sqlite3.Cursor)
        v = db.exec_sql('select * from user where name=:1', 'james')
        count = 0
        for i in v:
            # print(i)
            count += 1
        self.assertTrue(count == 0)
        del db

    def test_exec_sql_drop(self):
        # 删除数据表
        db = DBManager(file='test.db')
        v = db.exec_sql('CREATE TABLE TEMP (ID INTEGER PRIMARY KEY AUTOINCREMENT,NAME TEXT NOT NULL,PASSWORD TEXT NOT NULL);')
        self.assertEqual(type(v), sqlite3.Cursor)
        v = db.exec_sql('DROP TABLE TEMP')
        self.assertEqual(type(v), sqlite3.Cursor)
        del db

    def test_exec_sql_error1(self):
        # SQL语法错误
        db = DBManager(file='test.db')
        v = db.exec_sql('select * frome user where name=:1', 'admin')
        self.assertEqual(v, None)
        del db

    def test_exec_sql_error2(self):
        # SQL执行错误
        db = DBManager(file='test.db')
        v = db.exec_sql('select * from users where name=:1', 'admin')
        self.assertEqual(v, None)
        del db


if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(MyTestCase("test_exec_sql_select"))
    # suite.addTest(MyTestCase("test_exec_sql_insert"))
    # suite.addTest(MyTestCase("test_exec_sql_update"))
    # suite.addTest(MyTestCase("test_exec_sql_delete"))
    # suite.addTest(MyTestCase("test_exec_sql_drop"))
    # suite.addTest(MyTestCase("test_exec_sql_error1"))
    # suite.addTest(MyTestCase("test_exec_sql_error2"))
    # unittest.TextTestRunner(verbosity=3).run(suite)
