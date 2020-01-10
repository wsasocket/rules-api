import unittest
from time import sleep
from base64 import b64encode
from apps.v2.operation.user_mgr import UserManager

USER_TOKEN = None


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_1generate_user_token(self):
        global USER_TOKEN
        mgr = UserManager()
        mgr.timeout = 5
        USER_TOKEN = mgr.generate_user_token('james')
        self.assertIsInstance(USER_TOKEN, str)
        self.assertTrue(len(USER_TOKEN) > 5)

    def test_2check_user_token(self):
        global USER_TOKEN
        mgr = UserManager()
        mgr.timeout = 5
        USER_TOKEN = mgr.generate_user_token('james')
        t = mgr.check_user_token(USER_TOKEN)
        self.assertTrue(t == 0)
        count = 2
        while count > 0:
            sleep(5)
            count -= 1
        t = mgr.check_user_token(USER_TOKEN)
        self.assertTrue(t == -1)

    def test_3refresh_user_token(self):
        global USER_TOKEN
        mgr = UserManager()
        mgr.timeout = 10
        USER_TOKEN = mgr.generate_user_token('james')
        self.assertIsInstance(USER_TOKEN, str)
        self.assertTrue(len(USER_TOKEN) > 5)

        count = 3
        while count > 0:
            sleep(5)
            count -= 1
            mgr.refresh_user_token()
        t = mgr.check_user_token(USER_TOKEN)
        self.assertTrue(t == 0)

    def test_4user_login(self):
        global USER_TOKEN
        mgr = UserManager()
        mgr.timeout = 10
        l = mgr.login_validate('james', b64encode(b'helloworld').decode())
        self.assertTrue(l)
        l = mgr.login_validate('admin', b64encode(b'helloworld').decode())
        self.assertTrue(not l)

    def test_5check_user_right(self):
        global USER_TOKEN
        mgr = UserManager()
        mgr.timeout = 10
        USER_TOKEN = mgr.generate_user_token('james')
        r = mgr.check_user_right(USER_TOKEN, 0)
        self.assertTrue(r)
        r = mgr.check_user_right(USER_TOKEN, 1)
        self.assertTrue(r)
        r = mgr.check_user_right(USER_TOKEN, 2)
        self.assertTrue(not r)
        r = mgr.check_user_right(USER_TOKEN, 3)
        self.assertTrue(not r)
        r = mgr.check_user_right(USER_TOKEN, 4)
        self.assertTrue(not r)
        r = mgr.check_user_right(USER_TOKEN, 5)
        self.assertTrue(not r)

        USER_TOKEN = mgr.generate_user_token('admin')
        r = mgr.check_user_right(USER_TOKEN, 0)
        self.assertTrue(r)
        r = mgr.check_user_right(USER_TOKEN, 1)
        self.assertTrue(r)
        r = mgr.check_user_right(USER_TOKEN, 2)
        self.assertTrue( r)
        r = mgr.check_user_right(USER_TOKEN, 3)
        self.assertTrue( r)
        r = mgr.check_user_right(USER_TOKEN, 4)
        self.assertTrue( r)
        r = mgr.check_user_right(USER_TOKEN, 5)
        self.assertTrue(not r)

if __name__ == '__main__':
    # 设置一个定时器用于测试时TOKEN过期的功能
    # 初始化sched模块的 scheduler 类
    # 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
    unittest.main()
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(task, 'interval', seconds=10)
    # scheduler.start()

    # suite = unittest.TestSuite()
    # suite.addTest(MyTestCase("test_4user_right"))
    # # suite.addTest(MyTestCase("test_check_user_token"))
    # # suite.addTest(MyTestCase("test_exec_sql_update"))
    # # suite.addTest(MyTestCase("test_exec_sql_delete"))
    # # suite.addTest(MyTestCase("test_exec_sql_drop"))
    # # suite.addTest(MyTestCase("test_exec_sql_error1"))
    # # suite.addTest(MyTestCase("test_exec_sql_error2"))
    # unittest.TextTestRunner(verbosity=3).run(suite)
