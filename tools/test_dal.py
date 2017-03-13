# coding=utf-8
from dal.dal import oj_dal

params = {
    'username': '111',
}

oj_dal.insert('user', params, on_duplicate_update=False)