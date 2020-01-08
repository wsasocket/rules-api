import unittest
from apps.v2.operation.database_mgr import DBManager
import os
import sqlite3


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
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

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove('test.db')
        except FileNotFoundError:
            pass

    def test_exec_sql(self):
        db = DBManager()
        db.connect('test.db')
        v = db.exec_sql('select * from user where name=:1', ['admin'])
        self.assertEqual(type(v), list)


if __name__ == '__main__':
    unittest.main()
