from oj.server_settings import DATABASES
from dal_base import BaseDAL

oj_conn_args = {
    "name": DATABASES['default']['NAME'],
    "host": DATABASES['default']['HOST'],
    "port": DATABASES['default']['PORT'],
    "user": DATABASES['default']['USER'],
    "passwd": DATABASES['default']['PASSWORD'],
    'charset': 'utf8mb4'
}

submission_db_conn_args = {
    "name": DATABASES['submission']['NAME'],
    "host": DATABASES['submission']['HOST'],
    "port": DATABASES['submission']['PORT'],
    "user": DATABASES['submission']['USER'],
    "passwd": DATABASES['submission']['PASSWORD'],
    'charset': 'utf8mb4'
}

class OJDal(BaseDAL):
    def __init__(self, db_conn_args, logger=None):
        super(BaseDAL, self).__init__(**db_conn_args)

oj_dal = OJDal(oj_conn_args)
