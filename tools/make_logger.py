# -*- coding: utf-8 -*-

import logging


class Logger:
    @staticmethod
    def get_logger(name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        # if not os.path.exists("./log"):
        #     os.makedirs("./log")
        # fh = logging.FileHandler("./log/server.log")
        # fh = TimedRotatingFileHandler("./log/server.log", when='S', interval=3, backupCount=5)
        ch = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
        # fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # logger.addHandler(fh)
        logger.addHandler(ch)

        return logger
