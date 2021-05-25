from dao.mysql_dao import MysqlDao
from conf.global_config import g_conf


class MysqlTest:
    DB_NAME = "test_db"
    TB_NAME = "test_table"
    TB_PARAMS = "id INT PRIMARY KEY,name VARCHAR(32)"
    DROP_DB = "DROP DATABASE IF EXISTS %s;" % DB_NAME
    CREATE_DB = "CREATE DATABASE IF NOT EXISTS %s;" % DB_NAME
    USE_DB = "USE %s;" % DB_NAME
    CREATE_TB = "CREATE TABLE IF NOT EXISTS %s(%s);" % (TB_NAME, TB_PARAMS)
    DB_D = None

    @staticmethod
    def init():
        host = g_conf["db"]["host"]
        port = g_conf["db"]["port"]
        user = g_conf["db"]["user"]
        password = g_conf["db"]["password"]
        db = MysqlDao(host=host, port=port, user=user, password=password)
        db.connect_db()
        db.execute(MysqlTest.DROP_DB)
        db.execute(MysqlTest.CREATE_DB)
        db.execute_many([MysqlTest.USE_DB, MysqlTest.CREATE_TB])
        db.execute("show engines;")
        db.execute(" show variables like '%storage_engine%';")  # 查看当前默认存储引擎

        MysqlTest.DB_D = db

    @staticmethod
    def insert(id, name):
        sql = "INSERT INTO %s.%s(id, name) VALUES(%s, %s);" % (MysqlTest.DB_NAME, MysqlTest.TB_NAME, id, name)
        MysqlTest.DB_D.execute(sql)

    @staticmethod
    def query_all():
        sql = "SELECT * FROM %s.%s;" % (MysqlTest.DB_NAME, MysqlTest.TB_NAME)
        MysqlTest.DB_D.execute(sql)

    @staticmethod
    def insert_test():
        MysqlTest.insert(1, "1")
        MysqlTest.insert(2, "2")
        MysqlTest.insert(3, "3")

    @staticmethod
    def query_test():
        MysqlTest.query_all()

    @staticmethod
    def test1():  # 验证事务隔离级别
        pass
