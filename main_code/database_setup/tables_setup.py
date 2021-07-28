from main_code.utils.sql_utils import establish_connection, sql_run


def set_up_tables():
    # Establish connection to SQL
    connection = establish_connection()

    # Set up database
    _set_up_database(connection)

    # Create the books table
    _set_up_books_tables(connection)

    # Create the description table
    _set_up_descriptions_table(connection)

    # Create the genre table
    _set_up_genres_table(connection)

    # Create the books_genre table
    _set_up_books_genres_table(connection)

    # Create the rating_info table
    _set_up_rating_info_table(connection)

    connection.close()


def _set_up_database(connection):
    # remove the database Good_Reads_Data if it exists
    sql_run(connection, "DROP database IF EXISTS Good_Reads_Data;")
    # create the good_reads_data database
    print('Creating Good_Reads_Data database...', end='')
    sql_run(connection, "CREATE DATABASE Good_Reads_Data")
    connection.select_db("Good_Reads_Data")
    print('Done.')


def _set_up_books_tables(connection):
    print('Creating Books table...', end='')
    sql_run(connection, """CREATE TABLE
                               Books (
                                   book_id INT AUTO_INCREMENT PRIMARY KEY, 
                                   best_of VARCHAR(255), 
                                   title VARCHAR(255), 
                                   author VARCHAR(255), 
                                   average_rating FLOAT, 
                                   number_of_reviews INT,
                                   published_date VARCHAR(255),
                                   page_count INT
                               );""")
    print('Done.')


def _set_up_descriptions_table(connection):
    print('Creating Description table...', end='')
    sql_run(connection, """CREATE TABLE 
                           Description (
                               book_id INT PRIMARY KEY, 
                               description TEXT(4095),
                               FOREIGN KEY (book_id) 
                               REFERENCES Books(book_id)
                           );""")
    print('Done.')


def _set_up_genres_table(connection):
    print('Creating Genre table...', end='')
    sql_run(connection, """CREATE TABLE 
                           Genre ( 
                                genre_id INT AUTO_INCREMENT PRIMARY KEY,
                                genre VARCHAR(255)
                           );""")
    print('Done.')


def _set_up_books_genres_table(connection):
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
    print('Done.')


def _set_up_rating_info_table(connection):
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
    print('Done.')
