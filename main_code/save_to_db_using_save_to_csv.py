import csv

from selenium.common.exceptions import TimeoutException

from utils.utils import quiet_selenium_chrome_driver
from book_scraper import Book

from utils.sql_utils import sql_run, establish_connection

FROM_ROW = 0
TO_ROW = 400
# READING_FROM = '../project_data/links_to_books.csv'
READING_FROM = '../project_data/links_to_books.csv'



def is_in_db(book, connection):
    """
    Checks if the book is in the db of the given connection
    """
    is_exists = sql_run(connection, f"SELECT COUNT(1) FROM books WHERE title={book.name} and author={book.author};")
    return is_exists == 1


def add_book_to_db(book, connection):
    """
    add book to db using given connection
    """
    if is_in_db(book, connection):
        return False
    else:
        command = f"INSERT INTO books (book_link, best_of ,title,author,average_rating, number_of_reviews) VALUES " \
                  f"({book.link}, {book.top_of}, {book.name}, {book.author}, {book.rating.average_rating}, " \
                  f"{book.rating.number_of_reviews}); "
        sql_run(connection, command)
    return True


def add_rating_info_to_db(book, connection):
    command = f"INSERT INTO rating_info (book_number, rated_5, rated_4 ,rated_3 ,rated_2, rated_1) VALUES "
    for i in range(5):
        command += f"{book.rating.rating_histogram[5 - i]},"

    sql_run(connection, command)
    return True


def save_info_in_db():
    """
    fills up the given dictionary with scraped data
    """
    # reading from a file containing links to books
    with open(READING_FROM, newline='') as csv_file:
        reader = csv.reader(csv_file)
        driver = quiet_selenium_chrome_driver()
        connection = establish_connection()
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
                    print(f"adding book number {i} to books table")
                    add_book_to_db(book, connection)
                    print(f"adding book number {i} to rating table")
                    add_rating_info_to_db(book, connection)


        finally:
            driver.close()
            connection.close()


def main():
    save_info_in_db()



if __name__ == "__main__":
    main()
