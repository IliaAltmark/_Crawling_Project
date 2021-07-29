"""
Utility functions for the project
"""
import logging
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from main_code.config.config import DEFAULT_LOG_LEVEL, LOGGING_FORMAT, LOGGING_FILE_NAME


def quiet_selenium_chrome_driver():
    """
    Creates a quiet selenium chrome webdriver.
    :return: the driver
    """
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    return webdriver.Chrome(options=chrome_options)


def get_logger(name, output=LOGGING_FILE_NAME, level=DEFAULT_LOG_LEVEL):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Formatter
    formatter = logging.Formatter(LOGGING_FORMAT)

    # File Handler
    file_handler = logging.FileHandler(output)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Stream Handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.ERROR)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
