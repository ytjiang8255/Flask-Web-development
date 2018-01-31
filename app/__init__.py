#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from config import Config
from flask_mail import Mail
from flask_login import LoginManager
from flask_bootstrap import Bootstrap   #使用Flask-Bootstrap页面基本布局的基模板
from flask_moment import Moment     #使用Flask-Moment本地化日期和时间
from flask_babel import Babel, lazy_gettext as _l
import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler


app = Flask(__name__)
# app.config['SECRET_KEY'] = '123456'
app.config.from_object('config')
db = SQLAlchemy(app)     # 创建app.db
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')
mail = Mail(app)    #初始化一个 Mail 对象，这个对象为我们连接到 SMTP 服务器并且发送邮件
bootstrap = Bootstrap(app)
moment = Moment(app)
babel = Babel(app)

# 有些失败并不是结束于异常而且也不是主要问题，然而我们可能想要在日志中追踪它们以便做一些调试。
# 出于这个原因，我们还要为应用程序保持一个日志文件。
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        #  远程输出日志到邮件地址-SMTPHandler
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'],
            subject='Microblog Failure',
            credentials=auth,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    # 日志文件将会在 logs 目录，名称为 microblog.log。使用了 RotatingFileHandler 以至于生成的日志的大小是有限制的。
    # 在这个例子中，日志文件的大小限制在 1 兆，将保留最后 10 个日志文件作为备份。
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    # logging.Formatter 类能够定制化日志信息的格式。
    # 一个时间戳，日志记录级别和消息起源于以及日志消息和堆栈跟踪的文件和行号。
    # 后缀是一种数据格式输出具体格式
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO) #设置日志级别，默认为logging.WARNING
    app.logger.addHandler(file_handler) #日志输出到文件

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])
from app import views, models, errors

'''
日志级别大小关系为：CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET，当然也可以自己定义日志级别。
logging.basicConfig函数各参数:
filename: 指定日志文件名
filemode: 和file函数意义相同，指定日志文件的打开模式，'w'或'a'
format: 指定输出的格式和内容，format可以输出很多有用信息，如上例所示:
 %(levelno)s: 打印日志级别的数值
 %(levelname)s: 打印日志级别名称
 %(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
 %(filename)s: 打印当前执行程序名
 %(funcName)s: 打印日志的当前函数
 %(lineno)d: 打印日志的当前行号
 %(asctime)s: 打印日志的时间
 %(thread)d: 打印线程ID
 %(threadName)s: 打印线程名称
 %(process)d: 打印进程ID
 %(message)s: 打印日志信息
datefmt: 指定时间格式，同time.strftime()
level: 设置日志级别，默认为logging.WARNING
stream: 指定将日志的输出流，可以指定输出到sys.stderr,sys.stdout或者文件，默认输出到sys.stderr，当stream和filename同时指定时，stream被忽略


logging.StreamHandler: 日志输出到流，可以是sys.stderr、sys.stdout或者文件
logging.FileHandler: 日志输出到文件

日志回滚方式，实际使用时用RotatingFileHandler和TimedRotatingFileHandler
logging.handlers.BaseRotatingHandler
logging.handlers.RotatingFileHandler
logging.handlers.TimedRotatingFileHandler

logging.handlers.SocketHandler: 远程输出日志到TCP/IP sockets
logging.handlers.DatagramHandler:  远程输出日志到UDP sockets
logging.handlers.SMTPHandler:  远程输出日志到邮件地址
logging.handlers.SysLogHandler: 日志输出到syslog
logging.handlers.NTEventLogHandler: 远程输出日志到Windows NT/2000/XP的事件日志
logging.handlers.MemoryHandler: 日志输出到内存中的制定buffer
logging.handlers.HTTPHandler: 通过"GET"或"POST"远程输出到HTTP服务器
'''