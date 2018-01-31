#!/usr/bin/python3
# -*- coding: utf-8 -*-
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path

print(SQLALCHEMY_DATABASE_URI)
print(SQLALCHEMY_MIGRATE_REPO)
# sqlite:////home/clark/Desktop/FlaskCode/app.db
# /home/clark/Desktop/FlaskCode/db_repository

# 编写一些 Python 脚本来调用迁移的 APIs
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))