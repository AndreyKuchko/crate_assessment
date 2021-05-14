import logging


def get_logger(level):
    """ Sets up logger object with console handler
    """
    logger = logging.getLogger()
    logger.setLevel(level)
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    return logger
