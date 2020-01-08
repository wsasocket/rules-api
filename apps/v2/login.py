from base64 import b64decode
from binascii import Error as binError

from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful.reqparse import request

from apps.v2.operation.user_mgr import UserManager

LOGIN_FAIL = 0
LOGIN_SUCCESS = 1


class Login(Resource):
    """v2/login 接口说明:
    输入参数为json格式:{'userid':'用户名称','password':'经过base64编码的用户口令'}
    输出格式为json格式:{'code': fields.Integer, 'message': fields.String,
                    'info': fields.Nested({'user_token': fields.String,'user_right': fields.List(fields.Integer)})}
    参数说明:
    user_token 为用户登录的凭据;
    user_right 代表用户对定义的接口和模块的访问许可，传递给前端用于界面控制。
    """
    # 定义输出结果的结构及属性，原则上比使用jsonify专业

    output_fields = {'code': fields.Integer, 'message': fields.String,
                     'info': fields.Nested({'user_token': fields.String, 'user_right': fields.List(fields.Integer)})}

    def __init__(self):
        self.input_json = None
        self.output_json = {'code': 0, 'message': "", 'info': {'user_token': "", 'user_right': []}}

    @marshal_with(output_fields)
    def post(self):
        # 函数中的参数可以通过设置路由控制，要求名称必须和路由设置的一致
        # 参数可以是通过URL、form、json等方法传递过来的，比较灵活
        self.input_json = request.get_json(force=True)
        if not self._validate_input():
            self.output_json['code'] = LOGIN_FAIL
            self.output_json['message'] = 'Login Fail'
        else:
            self._validate_login_status()
        print(self.__doc__)
        return self.output_json

    def _validate_input(self):
        userid = self.input_json['userid'].strip(' \t\n\r')
        try:
            password = b64decode(self.input_json['password'])
        except binError:
            return False
        v = ["'", '"', ' ', '\\']
        for x in v:
            if x in userid:
                return False
        if len(userid) > 16 or len(userid) < 5:
            return False
        if len(password) > 16 or len(password) < 6:
            return False
        return True

    def _validate_login_status(self):
        userid = self.input_json['userid'].strip(' \t\n\r')
        passwd = self.input_json['password'].strip(' \t\n\r')
        usr_mgr = UserManager()
        print(UserManager)
        user_right = None
        if usr_mgr.login_validate(userid, passwd):
            user_right = usr_mgr.get_usr_right(userid)

        if user_right is None:
            self.output_json['code'] = LOGIN_FAIL
            self.output_json['message'] = 'login fail'
        else:
            self.output_json['code'] = LOGIN_SUCCESS
            self.output_json['message'] = 'welcome'
            self.output_json['info']['user_token'] = usr_mgr.generate_user_token(userid)
            self.output_json['info']['user_right'] = user_right
