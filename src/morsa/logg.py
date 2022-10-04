import logging

def info_logg():
    logging.basicConfig(level=logging.INFO)
    return logging.info('This will get logged')