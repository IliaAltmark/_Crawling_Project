from utils.sql_utils import establish_connection, sql_run


# TODO:get user and password from command line


# TODO: build a function that create a table

def main():
    # establish connection to SQL
    connection = establish_connection()
    # create the good_reads_data database
    sql_run(connection, "CREATE DATABASE IF NOT EXISTS good_reads_data;")
    connection.select_db("good_reads_data")
    # books table
    # remove the table books if it exists
    sql_run(connection, "DROP TABLE IF EXISTS books;")
    # create the books table
    sql_run(connection, "CREATE TABLE IF NOT EXISTS books (book_number INT AUTO_INCREMENT PRIMARY "
                        "KEY, book_link VARCHAR(255),best_of VARCHAR(255),title VARCHAR(255),author VARCHAR(255),"
                        "average_rating FLOAT, "
                        "number_of_reviews INT, rated_5 INT, rated_4 INT,rated_3 INT,rated_2 INT,"
                        "rated_1 INT, "
                        "top_voted_genre VARCHAR(255), top_voted_votes INT,2nd_voted_genre VARCHAR(255), "
                        "2nd_voted_votes "
                        "INT,3nd_voted_genre VARCHAR(255), 3nd_voted_votes INT);")
    # description table
    # remove the table description if it exists
    sql_run(connection, "DROP TABLE IF EXISTS description;")
    # create the description table
    sql_run(connection,
            "CREATE TABLE IF NOT EXISTS description (book_number INT PRIMARY KEY, description "
            "VARCHAR(4095));")

    # category table
    # remove the table category if it exists
    sql_run(connection, "DROP TABLE IF EXISTS category;")
    # create the category table
    sql_run(connection, "CREATE TABLE IF NOT EXISTS category (top_of_category VARCHAR(255) PRIMARY KEY, "
                        "link VARCHAR(255));")

    connection.close()


if __name__ == "__main__":
    main()
