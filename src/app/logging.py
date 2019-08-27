import logging
import os


def get_logger() -> logging.Logger:
    """Utility method to get a properly configured logger instance"""

    level = os.environ.get('LOGGING_LEVEL', 'INFO')

    logging.basicConfig(format='[%(levelname)s %(asctime)s (%(name)s:%(lineno)d)]: %(message)s')
    logger = logging.getLogger()

    try:
        logger.setLevel(level.upper())
    except (TypeError, ValueError) as err:
        logger.setLevel('INFO')
        logger.error('Defaulting to INFO logging: %s', str(err))

    return logger
