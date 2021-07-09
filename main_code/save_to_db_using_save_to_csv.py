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
    command = f"SELECT COUNT(1) FROM books WHERE title={book.name} and author={book.author};"
    is_exists = sql_run(connection, command)
    # TODO should be dataframe or something..
    return is_exists == 1


def add_book_to_db(book, connection):
    """
    add book to books table using given connection
    """
    if is_in_db(book, connection):
        return -1
    else:
        command = f"INSERT INTO books (book_link, best_of ,title,author,average_rating, number_of_reviews) VALUES " \
                  f"({book.link}, {book.top_of}, {book.name}, {book.author}, {book.rating.average_rating}, " \
                  f"{book.rating.number_of_reviews}); "
        sql_run(connection, command)

        # return the book_number in db (the pk)
        command_get_book_number = "SELECT book_number FROM books ORDER BY book_number DESC LIMIT 1;"
        book_num = sql_run(connection, command_get_book_number)
    return book_num


def add_rating_info_to_db(book, connection, book_number):
    """
    add rating information to rating_info table using given connection
    """
    command = f"INSERT INTO rating_info (book_number, rated_5, rated_4 ,rated_3 ,rated_2, rated_1) VALUES ({book_number}"
    for i in range(5):
        command += f", {book.rating.rating_histogram[5 - i]}"
    command += ";"
    sql_run(connection, command)
    return True


def add_description_to_db(book, connection, book_number):
    """
    add description information to description table using given connection
    """
    command = f"INSERT INTO description (book_number, description) VALUES ({book_number}, {book.description}); "
    sql_run(connection, command)
    return True


def add_books_genre_info(book, connection, book_number):
    """
    add information about the book genres to book_genres table using given connection
    """
    genres_dict = book.genres
    # loop over the genres_dict and for each iteration add a row to the books_genres table
    for i, k in enumerate(genres_dict):
        command = f"INSERT INTO books_genre (book_id, genre, top_voted, top_voted_num) VALUES ({book_number},{k},{i + 1},{genres_dict[k]});"
        sql_run(connection, command)
    return True


def add_genre_info(book, connection):
    """
    add genres to genre table
    """
    pass


def enter_db(connection):
    """
    connect to good_reads_data database
    """
    sql_run(connection, "USE good_reads_data")
    print("entered to db")


def save_info_in_db():
    """
    save the books information in good_reads_data database
    """
    # reading from a file containing links to books
    with open(READING_FROM, newline='') as csv_file:
        reader = csv.reader(csv_file)
        driver = quiet_selenium_chrome_driver()

        # establish connection and use the good_reads_data database
        connection = establish_connection()
        enter_db(connection)

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

                    # adding book to books table and save his id number
                    print(f"adding book number {i} to books table")
                    book_number = add_book_to_db(book, connection)

                    # adding book rating to rating_info table
                    print(f"adding book number {i} to rating table")
                    add_rating_info_to_db(book, connection, book_number)

                    # adding book description to description table
                    print(f"adding book number {i} to description table")
                    add_description_to_db(book, connection, book_number)

                    # adding book genre to books_genre table
                    print(f"adding book number {i} to books_genre table")
                    add_books_genre_info(book, connection, book_number)

        finally:
            driver.close()
            connection.close()


def main():
    save_info_in_db()


if __name__ == "__main__":
    main()
