# Domains

DOMAIN = "https://www.goodreads.com"
URL_TOP = DOMAIN + "/choiceawards/best-books-2020"
URL_GENRE = DOMAIN + "/shelf/show/"
LOGIN_PAGE = DOMAIN + "/user/sign_in"
EMAIL = "yovow90213@eyeremind.com"
PASS = "123456789"
USER_AGENT = {'User-agent': 'Mozilla/5.0',
              'Accept-Language': 'en-US, en;q=0.5'}

# ???

FROM_ROW = 0
TO_ROW = 400

# Data paths

WRITING_TO = '../project_data/books_test.csv'

# Shell interface

SHELL_DESCRIPTION = 'Has several optional arguments for scraping specific' \
                    'genres. By default if no arguments are provided will' \
                    'scrape the "best books of 2020" page.'
SHELL_GENRE_HELP = 'genre -- Must be a string representing the ' \
                   'desired genre/shelf from Goodreads'
SHELL_PAGE_NUM_HELP = 'page_num -- The page number to be scraped ' \
                      '(E.g. goodreads.com/shelf/show/(genre)?page=1)'
SHELL_TO_PAGE_HELP = 'to_page -- To which page to scrape '
SHELL_RELOAD_TABLES_HELP = 'reset-tables -- reloads the sql tables'
