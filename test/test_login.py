import unittest
from base64 import b64encode
import requests


class MyTestCase(unittest.TestCase):

    # def __init__(self):
    #     self.url = 'http://127.0.0.1:8080'

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_login_OK(self):
        """正常登录"""
        url = 'http://127.0.0.1:8080/v2/login'
        password = b'helloworld'
        payload = {'userid': 'james', 'password': b64encode(password).decode()}
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            res = r.json()
            # print("ok\n", res)
            self.assertEqual(res['code'], 1)
        else:
            self.assertEqual(True, False)

    def test_login_user_err1(self):
        """登录用户名不符合要求"""
        url = 'http://127.0.0.1:8080/v2/login'
        payload = {'userid': 'ja', 'password': 'aGVsbG93b3JsZA=='}
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            res = r.json()
            # print("user 1\n", res)
            self.assertEqual(res['code'], 0)
        else:
            self.assertEqual(True, False)

    def test_login_user_err2(self):
        """登录用户名不符合要求"""
        payload = {'userid': 'james\'', 'password': 'aGVsbG93b3JsZA=='}
        url = 'http://127.0.0.1:8080/v2/login'
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            res = r.json()
            # print("user 2\n", res)
            self.assertEqual(res['code'], 0)
        else:
            self.assertEqual(True, False)

    def test_login_pass_err1(self):
        """password 解码错误"""
        payload = {'userid': 'james', 'password': 'aGV-sbG93'}
        url = 'http://127.0.0.1:8080/v2/login'
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            res = r.json()
            # print("pass 1\n", res)
            self.assertEqual(res['code'], 0)
        else:
            self.assertEqual(True, False)

    def test_login_user_err2(self):
        """password 错误"""
        payload = {'userid': 'james', 'password': 'bGVsbG93b3JsZA=='}
        url = 'http://127.0.0.1:8080/v2/login'
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            res = r.json()
            # print("pass 2\n", res)

            self.assertEqual(res['code'], 0)
        else:
            self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
