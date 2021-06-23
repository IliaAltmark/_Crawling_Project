"""
Authors: Ilia Altmark and Tovi Benoni
Uses the class Book for scraping from a list that contains links to books.
The scraped data is then saved to a csv
"""
import csv

from selenium.common.exceptions import TimeoutException

from utils import quiet_selenium_chrome_driver
from book_scraper import Book

FROM_ROW = 0
TO_ROW = 400
READING_FROM = '../project_data/links_to_books_test.csv'
WRITING_TO = '../project_data/books_test.csv'


def main():
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

    # reading from a file containing links to books
    with open(READING_FROM, newline='') as csv_file:
        reader = csv.reader(csv_file)
        driver = quiet_selenium_chrome_driver()
        try:
            for i, row in enumerate(reader):
                # used for scraping part of the list when needed
                if FROM_ROW <= i <= TO_ROW:

                    print(f"Scraping row number {i}...")

                    link = row[0]
                    try:
                        # creating an object Book and scraping the provided
                        # link
                        book = Book.book_from_link(link, driver)
                    except TimeoutException as ex:
                        print(ex)
                        print("Don't forget to check the last row in the csv!")
                        break

                    # saving the scraped data in the dictionary
                    book_dict['name'].append(
                        book.name)
                    book_dict['author'].append(
                        book.author)
                    book_dict['description'].append(
                        book.description)
                    book_dict['average_rating'].append(
                        book.rating.average_rating)
                    book_dict['number_of_reviews'].append(
                        book.rating.number_of_reviews)
                    book_dict['top_of'].append(row[1])
                    book_dict['rated_5'].append(
                        book.rating.rating_histogram[5])
                    book_dict['rated_4'].append(
                        book.rating.rating_histogram[4])
                    book_dict['rated_3'].append(
                        book.rating.rating_histogram[3])
                    book_dict['rated_2'].append(
                        book.rating.rating_histogram[2])
                    book_dict['rated_1'].append(
                        book.rating.rating_histogram[1])

                    genres = iter(book.genres)

                    top_voted_key = next(genres)
                    book_dict['top_voted_genre'].append(top_voted_key[0])
                    book_dict['top_voted_votes'].append(
                        book.genres[top_voted_key])

                    try:
                        second_voted_key = next(genres)
                        book_dict['2nd_voted_genre'].append(
                            second_voted_key[0])
                        book_dict['2nd_voted_votes'].append(
                            book.genres[second_voted_key])
                    except StopIteration:
                        book_dict['2nd_voted_genre'].append('None')
                        book_dict['2nd_voted_votes'].append('None')

                    try:
                        third_voted_key = next(genres)
                        book_dict['3rd_voted_genre'].append(third_voted_key[0])
                        book_dict['3rd_voted_votes'].append(
                            book.genres[third_voted_key])
                    except StopIteration:
                        book_dict['3rd_voted_genre'].append('None')
                        book_dict['3rd_voted_votes'].append('None')

        finally:
            driver.close()

    # opens or creates the file and saves all the scraped book info in
    # the csv
    with open(WRITING_TO, 'a', newline='',
              encoding='utf-8') as csv_file:

        writer = csv.writer(csv_file)
        writer.writerow(book_dict.keys())
        writer.writerows(zip(*book_dict.values()))


if __name__ == "__main__":
    main()
