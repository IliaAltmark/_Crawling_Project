"""
Utility functions for the project
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def quiet_selenium_chrome_driver():
    """
    Creates a quiet selenium chrome webdriver.
    :return: the driver
    """
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    return webdriver.Chrome(options=chrome_options)
