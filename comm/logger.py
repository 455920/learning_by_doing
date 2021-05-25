import logging
from conf.global_config import g_conf

logging.basicConfig(level=logging.DEBUG,
                    filename=g_conf["log"]["log_path"],
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger(__name__)
