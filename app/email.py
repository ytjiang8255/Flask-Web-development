from threading import Thread #运行异步任务
from flask import render_template
from flask_mail import Message
from app import app, mail
from flask_babel import _


def send_async_email(app, msg): # send_email 函数立即返回，发送邮件的工作移到后台处理。
    with app.app_context():
        mail.send(msg)

# 简单的邮件框架
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # 每次我们需要发送邮件的时候启动一个进程的资源远远小于启动一个新的发送邮件的整个过程，
    # 因此把 mail.send(msg) 调用移入线程中
    Thread(target=send_async_email, args=(app, msg)).start()

# 发送修改密码的函数
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(_('[Microblog] Reset Your Password'),
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               # 邮件的主体也是使用此函数来渲染视图中所有的 HTML 模板
               text_body=render_template('email/reset_password.txt', suser=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))
