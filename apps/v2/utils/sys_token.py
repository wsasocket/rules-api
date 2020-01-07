import threading
import uuid
from datetime import datetime

TOKEN_VALIDATE = 0
TOKEN_TIME_OUT = -1
TOKEN_INVALIDATE = -2


class sys_token(object):
    _instance_lock = threading.Lock()
    data_user = dict()
    data_csrf = dict()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(sys_token, "_instance"):
            with sys_token._instance_lock:
                if not hasattr(sys_token, "_instance"):
                    sys_token._instance = object.__new__(cls)
        return sys_token._instance

    def generate_login_token(self, username):
        uuid_string = str(uuid.uuid4())
        self.data_user[uuid_string] = [datetime.now(), username]
        return uuid_string

    def check_login_token(self, login_token, username):
        # TODO: refresh token data,remove old token
        if login_token in self.data_user.keys():
            delta_time = datetime.now() - self.data_user[login_token][0]
            # TODO: update user token NOT remove
            if delta_time.total_seconds() // 60 > 30:
                # great than 30 miniuts drop it
                self.data_user.pop(login_token)
                return TOKEN_TIME_OUT

            if username == self.data_user[login_token][1]:
                # validate and update time
                self.data_user[login_token][0] = datetime.now()
                return TOKEN_VALIDATE
        return TOKEN_INVALIDATE

    def generate_csrf_token(self, user):
        uuid_string = str(uuid.uuid4())
        self.data_csrf[uuid_string] = [datetime.now(), user]
        return uuid_string

    def check_csrf_token(self, csrf_token, user):

        if csrf_token in self.data_csrf.keys():
            print('find key', csrf_token)
            delta_time = datetime.now() - self.data_csrf[csrf_token][0]
            if delta_time.total_seconds() // 60 > 30:
                # great than 30 miniuts drop it
                self.data_csrf.pop(csrf_token)
                return TOKEN_TIME_OUT

            if user == self.data_csrf[csrf_token][1]:
                # validate and update time
                self.data_csrf.pop(csrf_token)
                return TOKEN_VALIDATE
        return TOKEN_INVALIDATE
