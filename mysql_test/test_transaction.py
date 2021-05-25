from mysql_test.mysql_test_class import MysqlTest
from comm.logger import logger

if __name__ == "__main__":
    logger.info("========================================")
    MysqlTest.init()
    MysqlTest.insert_test()
    MysqlTest.query_test()

    print("SELECT * FROM %s.%s;" % (MysqlTest.DB_NAME, MysqlTest.TB_NAME))
