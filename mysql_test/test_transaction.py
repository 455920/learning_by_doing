import time
from comm.logger import logger
from mysql_test.mysql_test_class import MysqlTest
from dao.mysql_dao import MysqlDao
from comm.logger import logger
from comm.mul_process import ProcessClass
from conf.global_config import g_conf

host = g_conf["db"]["host"]
port = g_conf["db"]["port"]
user = g_conf["db"]["user"]
password = g_conf["db"]["password"]


class TestTransaction:
    @staticmethod
    def work1():
        db = MysqlDao(host=host, port=port, user=user, password=password)
        time.sleep(1)
        start_time = time.time()
        logger.info("work1__begin")
        db.execute_tran(f"insert into {MysqlTest.DB_NAME}.{MysqlTest.TB_NAME}(id, name) values(4,4)")  # 不会锁
        logger.info("work1__insert")
        db.execute_tran(f"update {MysqlTest.DB_NAME}.{MysqlTest.TB_NAME} set name='4' where id='1'")  # 不是同行不会锁
        logger.info("work1__update")
        db.execute_tran(f"select * from {MysqlTest.DB_NAME}.{MysqlTest.TB_NAME} where id='2'")  # 快照读、不会锁
        logger.info("work1__update")
        db.tran_commit()
        end_time = time.time()
        logger.info(f"work1__commit, time:{end_time - start_time}")

    @staticmethod
    def work2():
        db = MysqlDao(host=host, port=port, user=user, password=password)
        db.execute_tran("begin;")
        logger.info("work2__begin")
        db.execute_tran(f"select * from {MysqlTest.DB_NAME}.{MysqlTest.TB_NAME} where id='2' for update")
        logger.info("work2__query_for_update")
        time.sleep(5)
        logger.info("work2__wait for 4s")
        logger.info("work2__commit")
        db.tran_commit()

    @staticmethod
    def work3():
        db = MysqlDao(host=host, port=port, user=user, password=password)
        time.sleep(1)
        start_time = time.time()
        # db.execute_tran("begin;")
        logger.info("work1__begin")
        db.execute_tran(f"insert into {MysqlTest.DB_NAME}.{MysqlTest.TB_NAME}(id, name) values(5, 5)")  # 会锁
        # db.execute_tran(f"select * from {MysqlTest.DB_NAME}.{MysqlTest.TB_NAME} where id='1'")  # 不会锁
        # db.execute_tran(f"update {MysqlTest.DB_NAME}.{MysqlTest.TB_NAME} set name='4' where id='1'")  # 会锁
        logger.info("work1__update")
        db.tran_commit()
        end_time = time.time()
        logger.info(f"work1__commit, time:{end_time - start_time}")

    @staticmethod
    def work4():
        db = MysqlDao(host=host, port=port, user=user, password=password)
        # db.execute_tran("begin;")
        logger.info("work2__begin")
        db.execute_tran(f"select * from {MysqlTest.DB_NAME}.{MysqlTest.TB_NAME} for update")
        logger.info("work2__query_for_update")
        time.sleep(5)
        logger.info("work2__wait for 4s")
        logger.info("work2__commit")
        db.tran_commit()

    @staticmethod
    def work5():
        db = MysqlDao(host=host, port=port, user=user, password=password)
        # db.execute_tran("begin;")
        logger.info("work2__begin")
        db.execute_tran(f"select * from {MysqlTest.DB_NAME}.{MysqlTest.TB_NAME} for update")
        logger.info("work2__query_for_update")
        time.sleep(5)
        logger.info("work2__wait for 4s")
        logger.info("work2__commit")
        db.tran_commit()

    @staticmethod
    def test1():
        ProcessClass.run(target=TestTransaction.work2, args=())
        ProcessClass.run(target=TestTransaction.work1, args=())

        ProcessClass.wait_process_quit()

    @staticmethod
    def test2():
        ProcessClass.run(target=TestTransaction.work4, args=())
        ProcessClass.run(target=TestTransaction.work3, args=())

        ProcessClass.wait_process_quit()


if __name__ == "__main__":
    logger.info("准备初始数据========================================")
    MysqlTest.init()
    MysqlTest.insert_test()
    MysqlTest.query_test()
    TestTransaction.test1()
    TestTransaction.test2()
