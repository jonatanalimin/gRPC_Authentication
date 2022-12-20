import json
import logging.config

from controller.server import Server


def setup_logging(default_path='config/logging.json'):
    """
    Configure logging setup
    """
    path = default_path
    with open(path, 'rt') as f:
        config = json.load(f)
    logging.config.dictConfig(config)


if __name__ == '__main__':
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting server...")
    Server().start()
