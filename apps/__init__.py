# 在v1中__init__.py
from flask import Blueprint
from flask_restful import Api

from apps.v1.test import Hello, World, Upload, Download


def register_views(app):
    # 注册当前视图的资源接入点
    api = Api(app)
    api.add_resource(World, '/world')
    api.add_resource(Upload, '/upload')
    api.add_resource(Hello, '/hello/<string:name>/<int:id>')
    api.add_resource(Download, '/download/<string:filename>')


def create_blueprint_v1():
    # 注册蓝图->v1版本
    bp_v1 = Blueprint('v1', __name__)
    register_views(bp_v1)
    return bp_v1
