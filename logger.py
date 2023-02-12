import logging

class Logger:
    def get_logger(self):
        formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%m-%y')
        handler = logging.FileHandler('history.log')
        handler.setFormatter(formatter)

        logger = logging.getLogger('history')
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger
        