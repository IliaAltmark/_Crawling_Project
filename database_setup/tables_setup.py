from main_code.sql_utils import establish_connection, sql_run


# TODO:get user and password from command line: done


def main():
    # establish connection to SQL
    connection = establish_connection()

    # remove the database Good_Reads_Data if it exists
    sql_run(connection, "DROP database IF EXISTS Good_Reads_Data;")
    # create the good_reads_data database
    print('Creating Good_Reads_Data database...', end='')
    sql_run(connection, "CREATE DATABASE Good_Reads_Data")
    connection.select_db("Good_Reads_Data")
    print('Done.')

    # books table
    # create the books table
    print('Creating Books table...', end='')
    # TODO remove books_link: done
    sql_run(connection, """CREATE TABLE
                           Books (
                               book_id INT AUTO_INCREMENT PRIMARY KEY, 
                               best_of VARCHAR(255), 
                               title VARCHAR(255), 
                               author VARCHAR(255), 
                               average_rating FLOAT, 
                               number_of_reviews INT
                           );""")
    print('Done.')

    # description table
    # create the description table
    print('Creating Description table...', end='')
    sql_run(connection, """CREATE TABLE 
                           Description (
                               book_id INT PRIMARY KEY, 
                               description TEXT(4095),
                               FOREIGN KEY (book_id) 
                               REFERENCES Books(book_id)
                           );""")
    print('Done.')

    # genre table
    # create the genre table
    print('Creating Genre table...', end='')
    sql_run(connection, """CREATE TABLE 
                           Genre ( 
                                genre VARCHAR(255) PRIMARY KEY
                           );""")
    print('Done.')

    # books_genre table
    # create the books_genre table
    print('Creating Books_Genre table...', end='')
    sql_run(connection, """CREATE TABLE 
                           Books_Genre (
                               id INT AUTO_INCREMENT PRIMARY KEY,
                               book_id INT, 
                               genre VARCHAR(255), 
                               top_voted INT, 
                               top_voted_num INT,
                               FOREIGN KEY (book_id) 
                               REFERENCES Books(book_id),
                               FOREIGN KEY (genre) 
                               REFERENCES Genre(genre)
                           );""")
    print('Done.')

    # rating_info table
    # create the rating_info table
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

    connection.close()


if __name__ == "__main__":
    main()
