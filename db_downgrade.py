#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 如果有数据库迁移的支持，当你准备发布新版的时候，
# 只需要录制一个新的迁移，拷贝迁移脚本到生产服务器上接着运行脚本，所有事情就完成了。

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))
