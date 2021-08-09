from main_code.utils.sql_utils import establish_connection, sql_run
from main_code.utils.utils import get_logger

logger = get_logger(__name__)


def set_up_tables():
    logger.debug('Started set_up_tables')

    # Establish connection to SQL
    try:
        connection = establish_connection()
    except:
        logger.critical('Failed to establish connection to the SQL server')
        print('Could not establish connection to the SQL server. Exiting')
        exit()
    logger.debug('Established connection to the SQL server')

    # Set up database
    _set_up_database(connection)

    # Create the books table
    _set_up_books_tables(connection)
    logger.debug('Created books table')

    # Create the description table
    _set_up_descriptions_table(connection)
    logger.debug('Created descriptions table')

    # Create the genre table
    _set_up_genres_table(connection)
    logger.debug('Created genres table')

    # Create the books_genre table
    _set_up_books_genres_table(connection)
    logger.debug('Created books_genres table')

    # Create the author table
    _set_up_authors_table(connection)
    logger.debug('Created authors table')

    # Create the books_authors table
    _set_up_books_authors_table(connection)
    logger.debug('Created books_authors table')

    # Create the rating_info table
    _set_up_rating_info_table(connection)
    logger.debug('Created rating_info table')

    connection.close()
    logger.debug('Successfully set up database. Connection closed.')


def _set_up_database(connection):
    logger.debug('Dropping old database if exists')
    # remove the database Good_Reads_Data if it exists
    sql_run(connection, "DROP database IF EXISTS Good_Reads_Data;")

    logger.debug('Creating database')
    # create the good_reads_data database
    print('Creating Good_Reads_Data database...', end='')
    sql_run(connection, "CREATE DATABASE Good_Reads_Data")
    connection.select_db("Good_Reads_Data")

    logger.debug('Created database')
    print('Done.')


def _set_up_books_tables(connection):
    logger.debug('Creating books table')
    print('Creating Books table...', end='')

    sql_run(connection, """CREATE TABLE
                               Books (
                                   book_id INT AUTO_INCREMENT PRIMARY KEY, 
                                   best_of VARCHAR(255), 
                                   title VARCHAR(255),  
                                   average_rating FLOAT, 
                                   number_of_reviews INT,
                                   published_date VARCHAR(255),
                                   page_count INT
                               );""")

    logger.debug('Created books table')
    print('Done.')


def _set_up_descriptions_table(connection):
    logger.debug('Creating descriptions table')
    print('Creating Description table...', end='')

    sql_run(connection, """CREATE TABLE 
                           Description (
                               book_id INT PRIMARY KEY, 
                               description TEXT(4095),
                               FOREIGN KEY (book_id) 
                               REFERENCES Books(book_id)
                           );""")

    sql_run(connection, """ALTER TABLE Description 
                           CONVERT TO CHARACTER SET utf8""")

    logger.debug('Created descriptions table')
    print('Done.')


def _set_up_genres_table(connection):
    logger.debug('Creating genre table')
    print('Creating Genre table...', end='')

    sql_run(connection, """CREATE TABLE 
                           Genre ( 
                                genre_id INT AUTO_INCREMENT PRIMARY KEY,
                                genre VARCHAR(255)
                           );""")

    logger.debug('Created genre table')
    print('Done.')


def _set_up_authors_table(connection):
    logger.debug('Creating authors table')
    print('Creating Authors table...', end='')

    sql_run(connection, """CREATE TABLE 
                           Authors ( 
                                author_id INT AUTO_INCREMENT PRIMARY KEY,
                                author VARCHAR(255)
                           );""")

    logger.debug('Created authors table')
    print('Done.')


def _set_up_books_genres_table(connection):
    logger.debug('Creating books_genres table')
    print('Creating Books_Genre table...', end='')

    sql_run(connection, """CREATE TABLE 
                               Books_Genre (
                                   id INT AUTO_INCREMENT PRIMARY KEY,
                                   book_id INT, 
                                   genre_id INT, 
                                   top_voted INT, 
                                   top_voted_num INT,
                                   FOREIGN KEY (book_id) 
                                   REFERENCES Books(book_id),
                                   FOREIGN KEY (genre_id) 
                                   REFERENCES Genre(genre_id)
                               );""")

    logger.debug('Created books_genres table')
    print('Done.')


def _set_up_books_authors_table(connection):
    logger.debug('Creating books_authors table')
    print('Creating Books_Authors table...', end='')

    sql_run(connection, """CREATE TABLE 
                               Books_Authors (
                                   id INT AUTO_INCREMENT PRIMARY KEY,
                                   book_id INT, 
                                   author_id INT, 
                                   FOREIGN KEY (book_id) 
                                   REFERENCES Books(book_id),
                                   FOREIGN KEY (author_id) 
                                   REFERENCES Authors(author_id)
                               );""")

    logger.debug('Created books_authors table')
    print('Done.')


def _set_up_rating_info_table(connection):
    logger.debug('Creating rating_info table')
    print('Creating Rating_Info table...', end='')

    sql_run(connection, """CREATE TABLE
                           Rating_Info (
                               book_id INT PRIMARY KEY, 
                               rated_5 INT, 
                               rated_4 INT, 
                               rated_3 INT, 
                               rated_2 INT, 
                               rated_1 INT,
                               FOREIGN KEY (book_id) 
                               REFERENCES Books(book_id)
                           );""")

    logger.debug('Created rating_info table')
    print('Done.')
