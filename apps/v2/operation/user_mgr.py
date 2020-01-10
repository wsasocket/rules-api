import threading
import uuid
from datetime import datetime
from hashlib import md5
from base64 import b64decode, b64encode

TOKEN_VALIDATE = 0
TOKEN_TIME_OUT = -1
TOKEN_INVALIDATE = -2
MODULE_COUNT = 5


class _UserManagerInterface(object):
    """用户管理接口"""
    # 单例模式，管理用户的token和权限控制
    _instance_lock = threading.Lock()
    _operate_lock = False

    def __init__(self):
        self.user_token = dict()
        self.user_right = dict()
        self.user_passwd = dict()
        self.TIMEOUT = 1800
        self._setup_user_right()
        self._setup_user_list()

    def __new__(cls, *args, **kwargs):
        if not hasattr(_UserManagerInterface, "_instance"):
            with _UserManagerInterface._instance_lock:
                if not hasattr(_UserManagerInterface, "_instance"):
                    _UserManagerInterface._instance = object.__new__(cls)
        return _UserManagerInterface._instance

    def login_validate(self, user, passwd):

        if user not in self.user_passwd.keys():
            return False
        m = md5()
        p = b64decode(passwd)
        m.update(b64decode(passwd))

        if self.user_passwd[user] == b64encode(m.digest()).decode():
            return True
        else:
            return False

    def generate_user_token(self, username):
        while UserManager._operate_lock:
            pass
        UserManager._operate_lock = True
        uuid_string = str(uuid.uuid4())
        self.user_token[uuid_string] = [datetime.now(), username]
        UserManager._operate_lock = False
        return uuid_string

    def update_user_token(self, uuid):
        if uuid in self.user_token.keys():
            while UserManager._operate_lock:
                pass
            UserManager._operate_lock = True
            name = self.user_token[uuid][1]
            self.user_token[uuid] = [datetime.now(), name]
            UserManager._operate_lock = False

    def refresh_user_token(self):
        while UserManager._operate_lock:
            pass
        UserManager._operate_lock = True
        for uuid in self.user_token.keys():
            delta_time = (t := datetime.now()) - self.user_token[uuid][0]
            if delta_time.total_seconds() > self.TIMEOUT:
                # 注意: 在迭代过程中删除是不行的
                # self.user_token.pop(uuid)
                self.user_token = {k: self.user_token[k] for k in self.user_token if k != uuid}
            else:
                self.user_token[uuid][0] = t
        UserManager._operate_lock = False

    def check_user_token(self, uuid):
        # 仅仅是查询，不需要查看lock
        if uuid in self.user_token.keys():
            delta_time = datetime.now() - self.user_token[uuid][0]
            if delta_time.total_seconds() > self.TIMEOUT:
                return TOKEN_TIME_OUT
        else:
            return TOKEN_INVALIDATE

        return TOKEN_VALIDATE

    def check_user_right(self, uuid, module_index):
        if module_index >= MODULE_COUNT or module_index < 0:
            return False
        if uuid in self.user_token.keys():
            name = self.user_token[uuid][1]
            if name in self.user_right.keys():
                if self.user_right[name][module_index] == 1:
                    return True
        return False

    def get_usr_right(self, user):
        if user in self.user_right.keys():
            return self.user_right[user]
        return None

    @property
    def timeout(self):
        return self.TIMEOUT

    @timeout.setter
    def timeout(self, t, /):
        self.TIMEOUT = t

    def _setup_user_right(self):
        # 初始化阶段装载到内存中
        # TODO 增加数据库查询功能，设置对应的权限清单
        fake_db = {'james': [1, 1, 0, 0, 0], 'admin': [1, 1, 1, 1, 1]}
        for user, right in fake_db.items():
            self.user_right[user] = right

    def _setup_user_list(self):
        # 初始化阶段装载到内存中
        # TODO 增加数据库查询功能，测试用户及密码是否正确
        fake_db = {'james': '/F4DjTilcDIIVEHn/nAQsA==', 'admin': '/OqSD3QStdp74M9CuMk3WQ=='}
        for user, passwd in fake_db.items():
            self.user_passwd[user] = passwd


class UserManager(_UserManagerInterface):
    """
    UserManager的使用方法
    这个类主要功能是维护一个管理用户信息的对象。
    主要功能：
    1、生产/更新/检查用户的TOKEN，用于维护用户登陆状态
    2、获取/检查用户对各个模块的使用权限
    3、刷新对象维护的TOKEN列表，过期删除
    在初始化阶段需要从数据库或其他数据源获取用户的口令HASH和权限，可以根据不同的数据来源完备下列两个函数
    _setup_user_right()
    _setup_user_list()
    在全局需要一个定时器（计划执行）机制，用于刷新TOKEN
    refresh_user_token
    用户对接口的操作也需要对TOKEN进行更新，保证TOKEN的过期时间在操作行为后的30分钟，如果不使用，每隔30分钟需要登陆一次
    update_user_token
    """
    pass
