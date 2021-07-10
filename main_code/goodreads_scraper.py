"""
Authors: Ilia Altmark and Tovi Benoni
wrapper for link_scraper and save_to_csv
scrapes the necessary links and saves book info
"""
# imports from project files
import link_scraper as ls
from save_to_db import save_info_in_db

# imports from packages
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Has several optional arguments for scraping specific '
                    'genres. By default if no arguments are provided will '
                    'scrape the "best books of 2020" page.')

    parser.add_argument('-g', '--genre',
                        help='genre -- Must be a string representing the '
                             'desired genre/shelf from Goodreads '
                             '(goodreads.com/shelf)',
                        type=str)
    parser.add_argument('-p', '--page_num',
                        help='page_num -- The page number to be scraped '
                             '(E.g. goodreads.com/shelf/show/(genre)?page=1)',
                        type=int)
    parser.add_argument('-t', '--to_page',
                        help='to_page -- To which page to scrape ',
                        type=int)
    args = parser.parse_args()

    if args.genre:
        links_to_books_genre = ls.get_links_to_books_genre(args.genre,
                                                           args.page_num,
                                                           args.to_page)
        save_info_in_db(links_to_books_genre)
    else:
        links_to_top_genres = ls.get_links_to_top_genres()
        links_to_top_books = ls.get_link_to_books(links_to_top_genres)
        save_info_in_db(links_to_top_books)


if __name__ == "__main__":
    main()
