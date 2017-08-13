import logging
import logging.config
import threading

import time

from clean import robbot
from kefu import customerService
#
# logging.config.fileConfig("logging.conf")  # 采用配置文件
#
# # create logger
# logger = logging.getLogger("simpleExample")
#
# # "application" code
# logger.debug("debug message")
# logger.info("info message")
# logger.error("error message")
# logger.critical("critical message")
if __name__=='__main__':
    threading.Thread(target=customerService.start).start()
    time.sleep(8)
    threading.Thread(target=robbot.start).start()
    while True:
        pass