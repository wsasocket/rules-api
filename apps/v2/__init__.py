# 在v1中__init__.py
from flask import Blueprint
from flask_restful import Api

from apps.v2.login import Login


def register_views(app):
    # 注册当前视图的资源接入点
    api = Api(app)
    api.add_resource(Login, '/login')
    # api.add_resource(Upload, '/upload')
    # api.add_resource(Hello, '/hello/<string:name>/<int:id>')
    # api.add_resource(Download, '/download/<string:filename>')


def create_blueprint_v2():
    # 注册蓝图->v2版本
    bp_v2 = Blueprint('v2', __name__)
    register_views(bp_v2)
    return bp_v2
