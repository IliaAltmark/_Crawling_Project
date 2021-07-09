from utils.sql_utils import establish_connection, sql_run


# TODO:get user and password from command line


def main():
    # establish connection to SQL
    connection = establish_connection()

    # create the good_reads_data database
    print('Creating good_reads_data database...', end='')
    sql_run(connection, "CREATE DATABASE IF NOT EXISTS good_reads_data")
    connection.select_db("good_reads_data")
    print('Done.')

    # books table
    # remove the table books if it exists
    sql_run(connection, "DROP TABLE IF EXISTS books;")
    # create the books table
    print('Creating books table...', end='')
    sql_run(connection, """CREATE TABLE IF NOT EXISTS 
                           books (book_number INT AUTO_INCREMENT PRIMARY KEY, 
                           book_link VARCHAR(255), 
                           best_of VARCHAR(255), 
                           title VARCHAR(255), 
                           author VARCHAR(255), 
                           average_rating FLOAT, 
                           number_of_reviews INT);""")
    print('Done.')

    # description table
    # remove the table description if it exists
    sql_run(connection, "DROP TABLE IF EXISTS description;")
    # create the description table
    print('Creating description table...', end='')
    sql_run(connection,
            "CREATE TABLE IF NOT EXISTS description (book_number INT PRIMARY KEY, description TEXT(4095));")
    print('Done.')

    # books_genre table
    # remove the table books_genre if it exists
    sql_run(connection, "DROP TABLE IF EXISTS books_genre;")
    # create the books_genre table
    print('Creating books_genre table...', end='')
    sql_run(connection,
            "CREATE TABLE IF NOT EXISTS books_genre (book_id INT, genre VARCHAR(255), top_voted INT, "
            "top_voted_num INT);")
    print('Done.')

    # genre table
    # remove the table genre if it exists
    sql_run(connection, "DROP TABLE IF EXISTS genre;")
    # create the genre table
    print('Creating genre table...', end='')
    sql_run(connection,
            "CREATE TABLE IF NOT EXISTS genre (genre_id INT AUTO_INCREMENT PRIMARY KEY, genre VARCHAR("
            "255));")
    print('Done.')

    # rating_info table
    # remove the table rating_info if it exists
    sql_run(connection, "DROP TABLE IF EXISTS rating_info;")
    # create the rating_info table
    print('Creating rating_info table...', end='')
    sql_run(connection,
            "CREATE TABLE IF NOT EXISTS rating_info (book_number INT PRIMARY KEY, rated_5 INT, "
            "rated_4 INT,rated_3 INT,rated_2 INT, rated_1 INT);")
    print('Done.')

    connection.close()


if __name__ == "__main__":
    main()
