from base64 import b64decode, b64encode
from binascii import Error as binError
from hashlib import md5

from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful.reqparse import request
from apps.v2.utils.sys_token import sys_token


class RulesOperation(Resource):

    def get(self):
        # 查询规则
        pass

    def post(self):
        # 添加规则
        pass

    def patch(self):
        # 修改规则本身
        pass
