#!/usr/bin/python3
# -*- coding: utf-8 -*-

# http://localhost:5000 网址
from app import app, db, cli
from app.models import User, Post


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}


if __name__ == '__main__':
    app.run(debug=True)


# 模块是对象，并且所有的模块都有一个内置属性 __name__。
# 一个模块的 __name__ 的值取决于您如何应用模块。
# 如果 import 一个模块，那么模块__name__ 的值通常为模块文件名，不带路径或者文件扩展名。
# 但是您也可以像一个标准的程序样直接运行模块，
# 在这种情况下, __name__ 的值将是一个特别缺省"__main__"。

# debug=True 调试模式开启
