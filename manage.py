from flask_script import Server, Manager, Shell

from apps import create_app

app = create_app('default')
manager = Manager(app=app)


def make_shell_context():
    return dict(app=app)


manager.add_command('runserver', Server(host='127.0.0.1', port=8080, use_debugger=True, use_reloader=True))
manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run(default_command='runserver')

    # 这里可以创建shell模式，在shell模式下可以使用命令删除或创建数据库
    # 删除的命令是：db.drop_all()，创建的命令是：db.create_all()
    # 创建和删除哪些表需要提前将ORM模型引入进来（就是加到make_shell_context函数里）
    # manager.run(default_command='shell')
