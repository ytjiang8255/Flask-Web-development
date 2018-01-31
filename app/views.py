#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User, Post
from app.email import send_password_reset_email
from werkzeug.urls import url_parse
from datetime import datetime
from flask_babel import _, get_locale

import http.client as client
import time
import os
'''
views-POST:    
    导入 Post 和 PostForm 类
    在与 index 视图函数相关联的两个路由上，我们接受 POST 请求，因为我们需要接受提交的 blog。
    当接受常规的 GET 请求的时候我们像以前一样的处理。当我们接收到一个表单的提交的时候，我们在数据库中插入一个新的 Post 记录。
    模板现在接受一个新的参数：form。
    有了重定向，我们迫使浏览器在表单提交后发送另外一个请求，即重定向页的请求。
    这是一个简单的 GET 请求，因此一个刷新动作将会重复 GET 请求而不是多次提交表单。
    这个小技巧避免了用户在提交 blog 后不小心触发刷新的动作而导致插入重复的 blog。
 
views-Paginate:     
    paginate 方法能够被任何查询调用。它接受三个参数:
    页数，从 1 开始，
    每一页的项目数，这里也就是说每一页显示的 blog 数，
    错误标志。如果是 True，当请求的范围页超出范围的话，一个 404 错误将会自动地返回到客户端的网页浏览器。如果是 False，返回一个空列表而不是错误。
    从 paginate 返回的值是一个 Pagination 对象。这个对象的 items 成员包含了请求页面项目(本文是指 blog)的列表。
    配置文件中添加一些决定每页显示的 blog 数的配置项(文件 config.py):# pagination
    POSTS_PER_PAGE = 3  #每页3个post用户

'''

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    #g.locale = str(get_locale())

# 首页视图
'''
    导入 Post 和 PostForm 类
    在与 index 视图函数相关联的两个路由上，我们接受 POST 请求，因为我们需要接受提交的 blog。
    当接受常规的 GET 请求的时候我们像以前一样的处理。当接收到一个表单的提交的时候，在数据库中插入一个新的 Post 记录。
    模板现在接受一个新的参数：form
    
重定向，我们迫使浏览器在表单提交后发送另外一个请求，即重定向页的请求。
这是一个简单的 GET 请求，因此一个刷新动作将会重复 GET 请求而不是多次提交表单。
这个小技巧避免了用户在提交 blog 后不小心触发刷新的动作而导致插入重复的 blog。

pageSize = request.args.get('pageSize', 1, type=int)
    通过request.args.get我们可以获取 url 中带的参数, 比如: http://localhost:9537/users?pageSize=20 携带的参数 pageSize, 值为20.
    request.args.get('pageSize', 1, type=int)意思就是从 url 中获取参数 pageSize 的值,
    如果参数不存在就使用默认值1, type=int来保证返回的默认值是整型数字

pagination = Role.query.paginate(pageSize, per_page=pageNum, error_out=False)
    SQLAlchemy中的查询对象query有一个方法, 叫paginate, 它的返回值是一个分页对象pagination, 
    Role.query.paginate(pageSize, per_page=pageNum, error_out=False) 的意思就是从数据表 Role 里查询, 
    第一个参数 pageSize 就是我们要查询的页数, 这里是使用上面从 url 中获取到的值, 如果这个值不存在就使用默认值1, 
    第二个参数 per_page 是每页要展示的个数, 这里也使用的是从 url 获取的参数 pageNum 的值, 如果不存在就使用默认值10, 
    第三个参数是 error_out, 意思是当查询的页数超过了总的页数范围的处理方式, 
    如果为 True, 就返回一个404错误, 如果为 False, 就返回一个空列表.

'''
host = 'www.baidu.com'
def get_realtimes(host):
    while True:
        conn = client.HTTPConnection(host)
        conn.request("GET", "/")
        r = conn.getresponse()
        ts = r.getheader('date')
        local_time = time.mktime(time.strptime(ts[5:], "%d %b %Y %H:%M:%S GMT")) + (8 * 60 * 60)
        #print(local_time)
        ltime = time.gmtime(local_time)
        dat = ' %d-%d-%d %d:%d:%d ' % \
              (ltime.tm_year, ltime.tm_mon, ltime.tm_mday, ltime.tm_hour + 8, ltime.tm_min, ltime.tm_sec)
        # os.system(dat)
        time.sleep(1)
        return dat


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
#ValueError: urls must start with a leading slash
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('index'))   #在数据库中插入一个新的 Post 后，将会重定向到首页

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE2'], False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url, prev_url=prev_url)
        # # Flask提供的render_template函数把Jinja2模板引擎集成到了程序中。
        # render_template函数的第一个参数是模板的文件名。
        # 随后的参数都是键值对，表示模板中变量对应的真实值。

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE2'], False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        #  Login and validate the user.登录和验证用户。用户应该是一个实例你`用户`类
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))  #print error info
            # rebuild DB_table
            db.drop_all()
            db.create_all()
            return redirect(url_for('login'))
        # Logs a user in. You should pass the actual user object to this.
        # If the user’s is_active property is False, they will not be logged in unless force is True.
        # This will return True if the log in attempt succeeds, and False if it fails (i.e. because the user is inactive).
        # login_user  Parameters:	user (object) – The user object to log in.
        #               remember (bool) – Whether to remember the user after their session expires. Defaults to False.
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# 登出
@app.route('/logout')
def logout():
    #  will be logged out and any cookies for the session will be cleaned up.
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_('Check your email for the instructions to reset your password'))
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/user/<username>')  #页面导航
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    # 在需要添加链接允许用户访问下一页以及/或者前一页
    # has_next：如果在目前页后至少还有一页的话，返回 True
    # has_prev：如果在目前页之前至少还有一页的话，返回 True
    # next_num：下一页的页面数
    # prev_num：前一页的页面数

    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'), form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username)) #
        return redirect(url_for('index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User {} not found.').format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('user', username=username))

