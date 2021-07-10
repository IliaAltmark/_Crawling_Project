from selenium.common.exceptions import TimeoutException

from utils import quiet_selenium_chrome_driver, FROM_ROW, TO_ROW
from book_scraper import Book
from sql_utils import sql_run, establish_connection


def is_in_db(book, connection):
    """
    Checks if the book is in the db of the given connection
    """
    command = """SELECT EXISTS (
                      SELECT * 
                      FROM Books 
                      WHERE title=%s and author=%s
                  );"""
    is_exists = sql_run(connection, command, (book.name, book.author))
    is_exists = list(is_exists[0].values())[0]
    # TODO check what type is returned and extract the number: done
    return is_exists == 1


def add_book_to_db(book, connection, genre):
    """
    add book to books table using given connection
    """
    if is_in_db(book, connection):
        return -1
    else:
        # TODO: Fix best of: fixed
        command = """INSERT INTO 
                      Books (
                          best_of, title, author, average_rating, 
                          number_of_reviews
                      ) VALUES (
                          %s, %s, %s, %s, %s
                      );"""
        sql_run(connection, command, (genre, book.name, book.author,
                                      book.rating.average_rating,
                                      book.rating.number_of_reviews))

        # return the book_number in db (the pk)
        command_get_book_number = """SELECT book_id 
                                     FROM Books 
                                     ORDER BY book_id
                                     DESC LIMIT 1
                                     ;"""
        book_id = sql_run(connection, command_get_book_number)

    return book_id[0]['book_id']


def add_description_to_db(book, connection, book_number):
    """
    add description information to description table using given connection
    """
    command = """INSERT INTO 
                  Description (
                      book_id, description
                  ) VALUES (
                      %s, %s
                  );"""
    sql_run(connection, command, (book_number, book.description))
    return True


def add_genre_info(book, connection):
    """
    add genres to genre table
    """
    for genre in book.genres:
        genre_str = ','.join(genre)
        command = """SELECT EXISTS (
                          SELECT * 
                          FROM Genre
                          WHERE genre=%s
                      );"""
        is_exists = sql_run(connection, command, genre_str)
        is_exists = list(is_exists[0].values())[0]

        if not is_exists:
            command_insert = """INSERT INTO 
                                  Genre (
                                      genre
                                  ) VALUES (
                                      %s
                                  );"""
            sql_run(connection, command_insert, genre_str)


def add_books_genre_info(book, connection, book_number):
    """
    add information about the book genres to book_genres table
    using given connection
    """
    genres_dict = book.genres
    # loop over the genres_dict and for each iteration add a row to the
    # books_genres table
    for i, k in enumerate(genres_dict):
        genre_str = ','.join(k)
        command = """INSERT INTO 
                      Books_Genre (
                          book_id, genre, top_voted, top_voted_num
                      ) VALUES (
                          %s, %s, %s, %s
                      );"""
        sql_run(connection, command, (book_number, genre_str,
                                      i + 1, genres_dict[k]))
    return True


def add_rating_info_to_db(book, connection, book_number):
    """
    add rating information to rating_info table using given connection
    """
    command = f"""INSERT INTO 
                  Rating_Info (
                      book_id, rated_5, rated_4 ,rated_3 ,rated_2, rated_1
                  ) VALUES (
                      {book_number}
                  """
    for i in range(5):
        command += f", {book.rating.rating_histogram[5 - i]}"
    command += ");"
    sql_run(connection, command)
    return True


def enter_db(connection):
    """
    connect to good_reads_data database
    """
    sql_run(connection, "USE Good_Reads_Data")
    print("entered to db")


def save_info_in_db(l_to_books_dict):
    """
    save the books information in good_reads_data database
    """
    # TODO: split into smaller functions: pending
    driver = quiet_selenium_chrome_driver()

    # establish connection and use the good_reads_data database
    connection = establish_connection()
    enter_db(connection)

    try:
        for genre, books in l_to_books_dict.items():
            if genre:
                print(f"Scraping: {genre}...")

            for i, link in enumerate(books):
                if FROM_ROW <= i <= TO_ROW:
                    print(f"Scraping row number {i}...")

                    try:
                        # creating an object Book and scraping the provided
                        # link
                        book = Book.book_from_link(link, driver)
                    except TimeoutException as ex:
                        print(ex)
                        continue

                    # adding book to books table and save his id number
                    print(f"adding book number {i} to Books table")
                    book_id = add_book_to_db(book, connection, genre)

                    if book_id == -1:
                        print('The book is already in DB')
                        continue

                    # adding book description to description table
                    print(f"adding book number {i} to Description table")
                    add_description_to_db(book, connection, book_id)

                    # adding book genre to genre table
                    print(f"adding book number {i} to Genre table")
                    add_genre_info(book, connection)

                    # adding book genre to books_genre table
                    print(f"adding book number {i} to Books_Genre table")
                    add_books_genre_info(book, connection, book_id)

                    # adding book rating to rating_info table
                    print(f"adding book number {i} to Rating table")
                    add_rating_info_to_db(book, connection, book_id)

    finally:
        driver.close()
        connection.close()
