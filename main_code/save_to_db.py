from selenium.common.exceptions import TimeoutException

from main_code.utils.utils import quiet_selenium_chrome_driver
from main_code.config.config import FROM_ROW, TO_ROW
from main_code.book_scraper import Book
from main_code.utils.sql_utils import sql_run, establish_connection


def is_in_db(book, connection):
    """
    Checks if the book is in the db of the given connection.
    :param book: a book object
    :param connection: a connection object to an sql server.
    :return True if the book is in the connection's DB, else False.
    """
    command = """SELECT EXISTS (
                      SELECT * 
                      FROM Books 
                      WHERE title=%s and author=%s
                  );"""
    is_exists = sql_run(connection, command, (book.name, book.author))
    is_exists = list(is_exists[0].values())[0]
    return is_exists == 1


def add_book_to_db(book, connection, genre):
    """
    Add book to books table using given connection.
    :param book: a book object
    :param connection: a connection object to an sql server.
    :param genre: the genre the book corresponds to.
    :return the id of the book in the database
    """
    if is_in_db(book, connection):
        return -1
    else:
        command = """INSERT INTO 
                      Books (
                          best_of, title, author, average_rating, 
                          number_of_reviews, published_date, page_count
                      ) VALUES (
                          %s, %s, %s, %s, %s, %s, %s
                      );"""
        sql_run(connection, command, (genre, book.name, book.author,
                                      book.rating.average_rating,
                                      book.rating.number_of_reviews,
                                      book.published_date,
                                      book.page_count))

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
    Add description information to description table using the given connection.
    :param book: a book object
    :param connection: a connection object to an sql server.
    :param book_number: the id number of the book in the database.
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
    Add the given book genres to genre table, in the given connection's database.
    :param book: a book object
    :param connection: a connection object to an sql server.
    """
    genres_ids = []
    for genre in book.genres:
        genre_str = ','.join(genre)
        command = """SELECT genre_id 
                        FROM Genre
                        WHERE genre=%s
                      ;"""
        genre_ids = sql_run(connection, command, genre_str)

        if len(genre_ids) == 0:
            command_insert = """INSERT INTO 
                                  Genre (
                                      genre
                                  ) VALUES (
                                      %s
                                  );"""
            id_value_query = "SELECT LAST_INSERT_ID();"
            sql_run(connection, command_insert, genre_str)
            genre_id = sql_run(connection, id_value_query)[0]['LAST_INSERT_ID()']
        else:
            genre_id = genre_ids[0]['genre_id']
        genres_ids.append(genre_id)
    return genres_ids


def add_books_genre_info(book, connection, book_number, genres_ids):
    """
    Add information about the book genres to book_genres table
    using given connection.
    :param genres_ids:
    :param book: a book object
    :param connection: a connection object to an sql server.
    :param book_number: the id number of the book in the database.
    """
    genres_dict = book.genres
    # loop over the genres_dict and for each iteration add a row to the
    # books_genres table
    for i, k in enumerate(genres_dict):
        genre_id = genres_ids[i]
        print(genre_id)
        command = """INSERT INTO 
                      Books_Genre (
                          book_id, genre_id, top_voted, top_voted_num
                      ) VALUES (
                          %s, %s, %s, %s
                      );"""
        sql_run(connection, command, (book_number, genre_id,
                                      i + 1, genres_dict[k]))
    return True


def add_rating_info_to_db(book, connection, book_number):
    """
    Add rating information to rating_info table using given connection.
    :param book: a book object
    :param connection: a connection object to an sql server.
    :param book_number: the id number of the book in the database.
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
    Connect the given connection to good_reads_data database.
    :param connection: a connection object to an sql server.
    """
    sql_run(connection, "USE Good_Reads_Data")
    print("entered to db")


def add_book_object_to_db(book, connection, genre, i):
    """
    Adds book information to database (tables: books, description, genre, books_genre, rating_info)
    :param book: a book object
    :param connection: a connection object to an sql server.
    :param genre: the genre the book corresponds to.
    :param: i: used for progress prints.
    """
    # adding book to books table and save his id number
    print(f"adding book number {i} to Books table")
    book_id = add_book_to_db(book, connection, genre)

    if book_id == -1:
        print('The book is already in DB')
        return None

    # adding book description to description table
    print(f"adding book number {i} to Description table")
    add_description_to_db(book, connection, book_id)

    # adding book genre to genre table
    print(f"adding book number {i} to Genre table")
    genres_ids = add_genre_info(book, connection)

    # adding book genre to books_genre table
    print(f"adding book number {i} to Books_Genre table")
    add_books_genre_info(book, connection, book_id, genres_ids)

    # adding book rating to rating_info table
    print(f"adding book number {i} to Rating table")
    add_rating_info_to_db(book, connection, book_id)

    return True


def save_info_in_db(l_to_books_dict):
    """
    Saves the books' information in good_reads_data database
    """
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
                        # creating an object Book and scraping the provided link
                        book = Book.book_from_link(link, driver)
                    except TimeoutException as ex:
                        print(ex)
                        continue
                    # adding book to database (tables: books, description, genre, books_genre, rating_info)
                    add_book_object_to_db(book, connection, genre, i)
    finally:
        driver.close()
        connection.close()
