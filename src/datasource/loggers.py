import logging
from sys import stdout

def setup_logger(name : str):
    handler =  logging.StreamHandler(stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] %(name)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)

    logger = logging.Logger(name)
    logger.addHandler(handler)
    return logger