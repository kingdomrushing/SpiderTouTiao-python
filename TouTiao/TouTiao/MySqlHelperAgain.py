import pymysql
"""定义MySqlHelper类，
"""
class MysqlHelper(object):
    def __init__(self, host, port, db, user, password, charset):
        """
        :param host: IP
        :param port: 端口
        :param db: 数据库名称
        :param user: 用户名
        :param password: 密码
        :param charset: 编码方式
        """
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password
        self.charset = charset
        self.conn = None
        self.cursor = None

    def open(self):
        """
        打开数据库连接，使用cursor()方法获取操作游标
        """
        self.conn = pymysql.connect(host=self.host, port=self.port, db=self.db, user=self.user,
                                    password=self.password, charset=self.charset)
        self.cursor = self.conn.cursor()

    def getCursor(self):
        """
        获取操作游标
        :return: 操作游标
        """
        return self.cursor

    def close(self):
        """
        关闭数据库连接和操作游标
        """
        self.cursor.close()
        self.conn.close()

    def cud(self, sql):
        """
        执行sql语句
        :param sql:  sql语句
        :param params: 参数
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print('OK')
        except Exception as e:
            print(e)

    def all(self, table):
        """
        获取数据库所有信息
        :param table: 表
        :return: 结果
        """
        try:
            sql = 'select * from %s' % table
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(e)

    def specific(self, sql):
        """
        执行特定sql语句
        :param sql: 语句
        :return: 结果
        """
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(e)