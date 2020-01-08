from base64 import b64decode, b64encode
from binascii import Error as binError
from hashlib import md5

from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful.reqparse import request
from apps.v2.utils.sys_token import sys_token


class ExportRuleSet(Resource):
    # 根据模板导出数据
    pass

