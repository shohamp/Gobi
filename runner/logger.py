import logging

logger = None


def init_logger():
    global logger
    logger = logging.getLogger("gobi")
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('GOBI - %(asctime)s - %(levelname)s - %(message)s')
    formatter.datefmt = '%d/%m/%Y %H:%M:%S'

    ch.setFormatter(formatter)

    logger.addHandler(ch)


def debug(msg):
    logger.debug(msg)


def info(msg):
    logger.info(msg)