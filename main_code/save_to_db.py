from selenium.common.exceptions import TimeoutException

from main_code.utils.utils import quiet_selenium_chrome_driver, get_logger
from main_code.config.config import FROM_ROW, TO_ROW
from main_code.book_scraper import Book
from main_code.utils.sql_utils import sql_run, establish_connection, autoinc_uniques_insertion

logger = get_logger(__name__)


def is_in_db(book, connection):
    """
    Checks if the book is in the db of the given connection.
    :param book: a book object
    :param connection: a connection object to an sql server.
    :return True if the book is in the connection's DB, else False.
    """
    command = """SELECT EXISTS (
                                SELECT Books.title, Books.book_id, 
                                Books_Authors.author_id, Authors.author 
                                FROM Books 
                                JOIN Books_Authors on 
                                Books.book_id=Books_Authors.book_id 
                                JOIN Authors on 
                                Authors.author_id=Books_Authors.author_id 
                                WHERE title=%s and Authors.author=%s
                                );"""
    is_exists = sql_run(connection, command, (book.name, book.author[0]))
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
    logger.debug(f"Adding {book.link}'s data to the database")

    if is_in_db(book, connection):
        return -1
    else:
        command = """INSERT INTO 
                      Books (
                          best_of, title, average_rating, 
                          number_of_reviews, published_date, page_count
                      ) VALUES (
                          %s, %s, %s, %s, %s, %s
                      );"""
        sql_run(connection, command, (genre, book.name,
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

    logger.debug(f"Added {book.link}'s data to the database")
    return book_id[0]['book_id']


def add_description_to_db(book, connection, book_number):
    """
    Add description information to description table using the given connection.
    :param book: a book object
    :param connection: a connection object to an sql server.
    :param book_number: the id number of the book in the database.
    """
    logger.debug(f"{book.link} : adding description")

    command = """INSERT INTO 
                  Description (
                      book_id, description
                  ) VALUES (
                      %s, %s
                  );"""
    sql_run(connection, command, (book_number, book.description))

    logger.debug(f"{book.link} : added description")
    return True


def add_genre_info(book, connection):
    """
    Add the given book genres to genre table, in the given connection's database.
    :param book: a book object
    :param connection: a connection object to an sql server.
    """
    logger.debug(f"{book.link} : adding genre info")

    data = [','.join(genre) for genre in book.genres]
    res = autoinc_uniques_insertion(connection, 'Genre', 'genre_id', 'genre', data)

    logger.debug(f"{book.link} : added genre info")
    return res


def add_books_genre_info(book, connection, book_number, genres_ids):
    """
    Add information about the book genres to book_genres table
    using given connection.
    :param genres_ids:
    :param book: a book object
    :param connection: a connection object to an sql server.
    :param book_number: the id number of the book in the database.
    """
    logger.debug(f"{book.link} : adding books-genres info")

    genres_dict = book.genres
    # loop over the genres_dict and for each iteration add a row to the
    # books_genres table
    for i, k in enumerate(genres_dict):
        genre_id = genres_ids[i]
        command = """INSERT INTO 
                      Books_Genre (
                          book_id, genre_id, top_voted, top_voted_num
                      ) VALUES (
                          %s, %s, %s, %s
                      );"""
        sql_run(connection, command, (book_number, genre_id,
                                      i + 1, genres_dict[k]))

    logger.debug(f"{book.link} : added books-genres info")
    return True


def add_author_info(book, connection):
    """
    Add the given book authors to authors table, in the given connection's database.
    :param book: a book object
    :param connection: a connection object to an sql server.
    """
    logger.debug(f"{book.link} : adding authors")

    res = autoinc_uniques_insertion(connection, 'Authors', 'author_id', 'author', book.author)

    logger.debug(f"{book.link} : added authors info")
    return res


def add_books_authors_info(book, connection, book_number, authors_ids):
    """
    Add information about the book genres to book_genres table
    using given connection.
    :param authors_ids:
    :param book: a book object
    :param connection: a connection object to an sql server.
    :param book_number: the id number of the book in the database.
    """
    # loop over the genres_dict and for each iteration add a row to the
    # books_genres table
    logger.debug(f"{book.link} : adding books-authors info")

    for i in range(len(book.author)):
        author_id = authors_ids[i]
        command = f"""INSERT INTO 
                      Books_Authors (
                          book_id, author_id
                      ) VALUES (
                          {book_number}, {author_id}
                      );"""
        sql_run(connection, command)

    logger.debug(f"{book.link} : added books-authors info")
    return True


def add_rating_info_to_db(book, connection, book_number):
    """
    Add rating information to rating_info table using given connection.
    :param book: a book object
    :param connection: a connection object to an sql server.
    :param book_number: the id number of the book in the database.
    """
    logger.debug(f"{book.link} : adding rating info")

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

    logger.debug(f"{book.link} : added rating info")
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
    :param i: used for progress prints.
    """
    logger.debug(f"{book.link} : Starting to add information to the database")

    # adding book to books table and save his id number
    book_id = add_book_to_db(book, connection, genre)

    if book_id == -1:
        print('The book is already in DB')
        return None

    # adding book description to description table
    add_description_to_db(book, connection, book_id)

    # adding book genre to genre table
    genres_ids = add_genre_info(book, connection)

    # adding book genre to books_genre table
    add_books_genre_info(book, connection, book_id, genres_ids)

    # adding book author to authors table
    authors_ids = add_author_info(book, connection)

    # adding book genre to books_genre table
    add_books_authors_info(book, connection, book_id, authors_ids)

    # adding book rating to rating_info table
    add_rating_info_to_db(book, connection, book_id)

    logger.debug(f"{book.link} : Successfully added information to the database")
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
