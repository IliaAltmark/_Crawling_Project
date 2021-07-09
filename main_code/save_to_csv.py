"""
Authors: Ilia Altmark and Tovi Benoni
Uses the class Book for scraping from a list that contains links to books.
The scraped data is then saved to a csv
"""
# imports from project files
import utils as u

# imports from packages
import csv
from selenium.common.exceptions import TimeoutException
<<<<<<< HEAD
from utils import quiet_selenium_chrome_driver
=======

from utils.utils import quiet_selenium_chrome_driver
>>>>>>> origin/database_impl
from book_scraper import Book


def create_dict(b_dict, l_to_books_dict):
    """
    fills up the given dictionary with scraped data
    """
    # reading from a file containing links to books
    driver = quiet_selenium_chrome_driver()
    try:
        for genre, books in l_to_books_dict.items():
            if genre:
                print(f"Scraping: {genre}...")

            for i, link in enumerate(books):
                if u.FROM_ROW <= i <= u.TO_ROW:
                    print(f"Scraping row number {i}...")

                    try:
                        # creating an object Book and scraping the provided
                        # link
                        book = Book.book_from_link(link, driver)
                    except TimeoutException as ex:
                        print(ex)
                        print("Don't forget to check the last row in the csv!")
                        break

                    # saving the scraped data in the dictionary
                    b_dict['name'].append(
                        book.name)
                    b_dict['author'].append(
                        book.author)
                    b_dict['description'].append(
                        book.description)
                    b_dict['average_rating'].append(
                        book.rating.average_rating)
                    b_dict['number_of_reviews'].append(
                        book.rating.number_of_reviews)
                    b_dict['top_of'].append(genre)
                    b_dict['rated_5'].append(
                        book.rating.rating_histogram[5])
                    b_dict['rated_4'].append(
                        book.rating.rating_histogram[4])
                    b_dict['rated_3'].append(
                        book.rating.rating_histogram[3])
                    b_dict['rated_2'].append(
                        book.rating.rating_histogram[2])
                    b_dict['rated_1'].append(
                        book.rating.rating_histogram[1])

                    genres = iter(book.genres)

                    try:
                        top_voted_key = next(genres)
                        b_dict['top_voted_genre'].append(top_voted_key[0])
                        b_dict['top_voted_votes'].append(
                            book.genres[top_voted_key])
                    except StopIteration:
                        b_dict['top_voted_genre'].append(None)
                        b_dict['top_voted_genre'].append(None)

                    try:
                        second_voted_key = next(genres)
                        b_dict['2nd_voted_genre'].append(
                            second_voted_key[0])
                        b_dict['2nd_voted_votes'].append(
                            book.genres[second_voted_key])
                    except StopIteration:
                        b_dict['2nd_voted_genre'].append(None)
                        b_dict['2nd_voted_votes'].append(None)

                    try:
                        third_voted_key = next(genres)
                        b_dict['3rd_voted_genre'].append(third_voted_key[0])
                        b_dict['3rd_voted_votes'].append(
                            book.genres[third_voted_key])
                    except StopIteration:
                        b_dict['3rd_voted_genre'].append(None)
                        b_dict['3rd_voted_votes'].append(None)

    finally:
        driver.close()


def create_csv(b_dict):
    """
    saves the scraped data from the given dictionary to a csv
    """
    with open(u.WRITING_TO, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(b_dict.keys())
        writer.writerows(zip(*b_dict.values()))
