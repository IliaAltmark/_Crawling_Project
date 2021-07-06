"""
Authors: Ilia Altmark and Tovi Benoni
wrapper for link_scraper and save_to_csv
scrapes the necessary links and saves book info
"""
# imports from project files
import link_scraper as ls
from save_to_csv import create_dict, create_csv

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

    links_to_books_genre = None
    links_to_top_books = None

    if args.genre:
        links_to_books_genre = ls.get_links_to_books_genre(args.genre,
                                                           args.page_num,
                                                           args.to_page)
    else:
        links_to_top_genres = ls.get_links_to_top_genres()
        links_to_top_books = ls.get_link_to_books(links_to_top_genres)

    # declaring a dictionary which will contain lists of scraped data.
    # each list contains data scraped from the same place in the HTML
    book_dict = {'name': [], 'author': [], 'description': [],
                 'average_rating': [], 'number_of_reviews': [],
                 'top_of': [],
                 'rated_5': [], 'rated_4': [], 'rated_3': [], 'rated_2': [],
                 'rated_1': [],
                 'top_voted_genre': [], 'top_voted_votes': [],
                 '2nd_voted_genre': [], '2nd_voted_votes': [],
                 '3rd_voted_genre': [], '3rd_voted_votes': []}

    if args.genre:
        create_dict(book_dict, links_to_books_genre)
    else:
        create_dict(book_dict, links_to_top_books)
    create_csv(book_dict)


if __name__ == "__main__":
    main()
