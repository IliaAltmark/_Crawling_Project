"""
Authors: Ilia Altmark and Tovi Benoni
wrapper for link_scraper and save_to_csv
scrapes the necessary links and saves book info
"""
# imports from project files
from link_scraper import get_links_to_top_genres, get_link_to_books
from save_to_csv import create_dict, create_csv


# imports from packages


def main():
    links_to_top_genres = get_links_to_top_genres()

    links_to_top_books = get_link_to_books(links_to_top_genres)

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

    create_dict(book_dict, links_to_top_books)
    create_csv(book_dict)


if __name__ == "__main__":
    main()
