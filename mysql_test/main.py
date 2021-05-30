import time
from comm.logger import logger
from mysql_test.mysql_test_class import MysqlTest
from comm.logger import logger
from mysql_test.test_transaction import TestTransaction

if __name__ == "__main__":
    logger.info("准备初始数据========================================")
    MysqlTest.init()
    MysqlTest.insert_test()
    MysqlTest.query_test()
    logger.info("行锁========================================")
    TestTransaction.test1()

    logger.info("表锁========================================")
    TestTransaction.test2()
