"""
Authors: Ilia Altmark and Tovi Benoni
wrapper for link_scraper and save_to_csv
scrapes the necessary links and saves book info
"""
# imports from project files
import main_code.link_scraper as ls
import main_code.database_setup.tables_setup as ts
from main_code.save_to_db import save_info_in_db
from main_code.config.config import SHELL_DESCRIPTION, \
    SHELL_GENRE_HELP, SHELL_PAGE_NUM_HELP, SHELL_TO_PAGE_HELP, \
    SHELL_RELOAD_TABLES_HELP
from main_code.utils.utils import get_logger

# imports from packages
import argparse

logger = get_logger(__name__)


def main():
    logger.info('Program has started.')
    # Setting up terminal interface using argparse.
    parser = argparse.ArgumentParser(
        description=SHELL_DESCRIPTION)

    parser.add_argument('-g', '--genre',
                        help=SHELL_GENRE_HELP,
                        type=str)
    parser.add_argument('-p', '--page_num',
                        help=SHELL_PAGE_NUM_HELP,
                        type=int)
    parser.add_argument('-t', '--to_page',
                        help=SHELL_TO_PAGE_HELP,
                        type=int)
    parser.add_argument('-r', '--reload-tables', action='store_true',
                        help=SHELL_RELOAD_TABLES_HELP,
                        )
    args = parser.parse_args()

    # Does a genre specific scrape or a full scrape.
    if args.reload_tables:
        ts.set_up_tables()
    if args.genre:
        links_to_books_genre = ls.get_links_to_books_genre(args.genre,
                                                           args.page_num,
                                                           args.to_page)
        save_info_in_db(links_to_books_genre)
    else:
        links_to_top_genres = ls.get_links_to_top_genres()
        links_to_top_books = ls.get_link_to_books(links_to_top_genres)
        save_info_in_db(links_to_top_books)

    logger.info('Program finished successfully')
