# 专心写好逻辑就好

import base64
import os

from flask import abort, make_response, send_from_directory
from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import inputs
from flask_restful import request
from flask_restful.reqparse import RequestParser
from werkzeug.datastructures import FileStorage
from flask import render_template

class Hello(Resource):
    # 定义输出结果的结构及属性，原则上比使用jsonify专业
    output_fields = {'name': fields.String, 'id': fields.Integer, 'more': fields.Nested({'a': fields.String})}

    @marshal_with(output_fields)
    def get(self, name=None, id=None):
        # 函数中的参数可以通过设置路由控制，要求名称必须和路由设置的一致
        # 参数可以是通过URL、form、json等方法传递过来的，比较灵活
        parser = RequestParser()
        # location = 'args' 'json' 'form'
        parser.add_argument('haha', type=str, help='Rate to charge for this resource', location="args")
        args = parser.parse_args()
        # abort(500,result='Invalid token',code=500)
        test = r'alert tcp $EXTERNAL_NET any -> $SQL_SERVERS 3306 (msg:"SERVER-MYSQL UDF function drop attempt"; flow:to_server,established; content:"|03|drop"; offset:4; nocase; content:"sys_"; within:50; fast_pattern; pcre:"/\x03drop\s+function(\s+if\s+exists)*\s+sys_(exec|eval|get|bineval|set)/im"; metadata:policy max-detect-ips drop, policy security-ips drop, service mysql; reference:url,github.com/rapid7/metasploit-framework/blob/master/modules/exploits/multi/mysql/mysql_udf_payload.rb; classtype:misc-activity; sid:45848; rev:1;)'
        testb64 = base64.b64encode(test.encode())
        return {'name': name, 'id': id, 'more': {'a': testb64.decode()}}


class World(Resource):
    output_fields = {'country': fields.String, 'code': fields.Integer,
                     'more': fields.Nested({'province': fields.String, 'urls': fields.Url})}

    # @marshal_with(output_fields)
    def get(self):

        # 参数可以是通过URL、form、json等方法传递过来的，比较灵活
        parser = RequestParser()
        # location = 'args' 'json' 'form'
        parser.add_argument('province', required=True, type=str, help='Tell me you Province!',
                            location="args")
        parser.add_argument('urls', required=True, type=str, help='Tel me You country URL', location="args")
        args = parser.parse_args(strict=True)
        print(args['urls'])
        print(request.full_path)
        print(request.url)

        try:
            inputs.url(args['urls'])
        except ValueError:
            abort(500, 'URL:{} is invalidate'.format(args['urls']))
        return {'country': 'China', 'code': 86010, 'more': {'province': args['province'], 'url': args['urls']}}


class Upload(Resource):

    def get(self):
        # 这里是在API内部，原则上不应当返回页面，主要是为了测试上传功能才被迫如此
        # 也可以在上面一层进行处理，这样就比较规范了
        # 实际上flask-restful默认返回的类型都是application/json
        # 不修改这个头部信息是不能看到正常的页面的
        response = make_response(render_template('upload.html'))
        response.headers["Content-Type"]= 'text/html'
        return response


    def post(self):
        parser = RequestParser()
        parser.add_argument('file', type=FileStorage, location='files')
        args = parser.parse_args()
        print(args)
        file = args['file']
        file.save(file.filename)
        return file.filename, 201


class Download(Resource):
    def get(self, filename):
        # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
        directory = os.getcwd()  # 假设在当前目录
        response = make_response(send_from_directory(directory, filename, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
        return response
