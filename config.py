#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
basedir = os.path.abspath(os.path.dirname(__file__))


SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 应用程序错误报告机制。就是当错误发生的时候发送电子邮件。在应用程序中配置邮件服务器以及管理员邮箱地址
MAIL_SERVER = os.environ.get('MAIL_SERVER') # mail server settings
MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
ADMINS = ['your-email@example.com'] # administrator list

LANGUAGES = ['en', 'es']

# 在配置文件中添加一些决定每页显示的 blog 数的配置项
POSTS_PER_PAGE = 2
POSTS_PER_PAGE2 = 3
'''
在一个没有邮件服务器的开发机器上测试上述代码是相当容易的，多亏了 Python 的 SMTP 调试服务器。
仅需要打开一个新的命令行窗口(Windows 用户打开命令提示符)接着运行如下内容打开一个伪造的邮箱服务器:

python -m smtpd -n -c DebuggingServer localhost:25

当邮箱服务器运行后，应用程序发送的邮件将会被接收到并且显示在命令行窗口上。
'''
