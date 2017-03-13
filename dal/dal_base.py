import threading
import MySQLdb
import codecs
codecs.register(
    lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)

def get_insert_sql(
    table, keys, on_duplicate_update=False,
        ignore=False, dup_unupdate_keys=[], primary_key=''):
    '''
    >>> get_insert_sql('foo', ['a', 'b'])
    'insert into foo (a, b) values (%s, %s)'
    >>> get_insert_sql(
    ...     'foo', ['a', 'b'], on_duplicate_update=True, primary_key='id')
    'insert into foo (a, b) values (%s, %s) \
ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id), a=values(a), b=values(b)'
    >>> get_insert_sql(
    ...     'foo', ['a', 'b'], on_duplicate_update=True,
    ...     dup_unupdate_keys=['a', ])
    'insert into foo (a, b) values (%s, %s) \
ON DUPLICATE KEY UPDATE b=values(b)'
    '''
    sql = 'insert into %s (%s) values (%s)' % (
        table, ', '.join(keys), ', '.join(['%s'] * len(keys)))
    if on_duplicate_update:
        odu_clause = ', '.join(
            '%s=values(%s)' % (k, k) for k in keys
            if k not in dup_unupdate_keys
            )
        id_prefix = '%s=LAST_INSERT_ID(%s), ' % (primary_key, primary_key) \
            if primary_key else ''
        odu_clause = ' ON DUPLICATE KEY UPDATE %s' % (id_prefix + odu_clause, )
        sql = sql + odu_clause
    return sql

class DAL(threading.local):
    def __init__(self, host, name, user, passwd, port=3306, charset='utf8'):
        self.host, self.port, self.name, self.user, self.passwd = \
            host, int(port), name, user, passwd
        self.conn_key = '%s:%s@%s:%s/%s' % (user, passwd, host, port, name)
        self.cursor = None
        self.conn = None
        self.charset = charset

    def open(self):
        global local_conn
        if not local_conn:
            local_conn = threading.local()
        if not hasattr(local_conn, 'connections'):
            local_conn.connections = {}
        conn = local_conn.connections.get(self.conn_key)
        if not conn:
            conn = MySQLdb.connect(
                host=self.host, port=self.port, user=self.user,
                passwd=self.passwd, db=self.name, charset=self.charset
                )
            conn.autocommit(True)
            local_conn.connections[self.conn_key] = conn

        self.conn = conn
        self.cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)

    def get_cursor(self):
        if not self.cursor:
            self.open()
        return self.cursor

    def execute(self, sql_fmt, *params):
        retry = 0
        while True:
            retry += 1
            try:
                # cursor = self.get_cursor() // 老代码
                self.get_cursor()
                self.cursor.execute(sql_fmt, params)
                break
            except:
                self.close()
                if retry >= 2:
                    raise

    def close(self):
        global local_conn
        if self.cursor:
            self.cursor.close()
            self.cursor = None

        if self.conn:
            conn = local_conn.connections.pop(self.conn_key, None)
            if conn:
                conn.close()
            self.conn = None

    # 需要支持事务
    def begin(self, ):
        self.get_cursor()
        self.conn.begin()

    def commit(self, ):
        self.get_cursor()
        self.conn.commit()

    def rollback(self, ):
        self.get_cursor()
        self.conn.rollback()

class BaseDAL(DAL):
    def insert(
        self, table, info, on_duplicate_update=False,
            unique_keys={}, dup_unupdate_keys=[]):
        if not info:
            return None, 'no values'
        try:
            sql = get_insert_sql(
                table, info.keys(), on_duplicate_update,
                dup_unupdate_keys=dup_unupdate_keys,
                primary_key='id',
                )
            self.execute(sql, *info.values())
            return self.cursor.connection.insert_id(), 'new insert'
        except MySQLdb.IntegrityError:
            if unique_keys:
                rs = self.fetchone(table, ['id', ], where=unique_keys)
                if rs:
                    return rs['id'], 'already exist, insert error'
            raise
        except:
            raise
