import logging

from sys import stdout
from logging import DEBUG, INFO, WARN, ERROR, FATAL
from logging import basicConfig, StreamHandler
from app.settings import SETTINGS

def setup():
    logging_level = INFO
    # Setting up logging
    basicConfig(
        level=logging_level,
        format="%(asctime)s - %(levelname)s - [%(module)s] - %(message)s",
        handlers=[
            StreamHandler(stdout)
        ]
    )