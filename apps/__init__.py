



# apps/v1/__init__.py 定义的 注册蓝图函数
# 下面的函数在 __init__.py 文件中定义
# 注册蓝图，也就是使用内部机制完成版本分离

from flask import Flask, render_template

from apps.v1 import create_blueprint_v1


def create_app(config_name):
    flask_app = Flask(__name__)
    # register_errors(flask_app)
    flask_app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')

    # 可以增加更多版本的蓝图
    @flask_app.route('/upload.html')
    def __test():
        return render_template('upload.html')
#         return '''<!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>Upload</title>
# </head>
# <body>
# <form method="POST" action="/v1/upload" enctype="multipart/form-data">
#     <input type="file" name="file">
#     <input type="submit">
# </form>
# </body>
# </html>'''

    return flask_app
