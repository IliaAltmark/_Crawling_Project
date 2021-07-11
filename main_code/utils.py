"""
Utility functions for the project
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DOMAIN = "https://www.goodreads.com"
URL_TOP = DOMAIN + "/choiceawards/best-books-2020"
URL_GENRE = DOMAIN + "/shelf/show/"
LOGIN_PAGE = DOMAIN + "/user/sign_in"
EMAIL = "yovow90213@eyeremind.com"
PASS = "123456789"
USER_AGENT = {'User-agent': 'Mozilla/5.0',
              'Accept-Language': 'en-US, en;q=0.5'}

FROM_ROW = 0
TO_ROW = 400
WRITING_TO = '../project_data/books_test.csv'


def quiet_selenium_chrome_driver():
    """
    Creates a quiet selenium chrome webdriver.
    :return: the driver
    """
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    return webdriver.Chrome(options=chrome_options)
