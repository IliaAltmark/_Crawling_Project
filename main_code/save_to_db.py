from main_code.book_scraper import Book
from utils.sql_utils import sql_run, establish_connection
from main_code.link_scraper import get_links_to_top_genres, get_link_to_books


def save_top_genres(connection):
    links = get_links_to_top_genres()
    for link in links:
        # extracts category name from the link
        category = link[link.rfind('/') + 6:]
        command = f"INSERT INTO category (top_of_category, link) Values ({category}, {link})"
        sql_run(connection, command)


def retrieve_top_genres_links(connection):
    return sql_run(connection, "SELECT link from category")


def save_books(connection):
    genres_links = [it.values() for it in retrieve_top_genres_links(connection)]
    genre_to_links = get_link_to_books(genres_links)

    for genre, links in genre_to_links.items():
        for link in links:
            book = Book.book_from_link(link, genre)
            add_book_to_db(book, connection)


def is_in_db(book, connection):
    """
    Checks if the book is in the db of the given connection
    """
    is_exists = sql_run(connection, f"SELECT COUNT(1) FROM books WHERE title={book.name} and author={book.author}")
    return is_exists == 1


def add_book_to_db(book, connection):
    """
    add book to db using given connection
    """
    if book.is_in_db(connection):
        return False
    else:
        command = "INSERT INTO books (book_link, best_of ,title,author,average_rating, number_of_reviews, rated_5, " \
                  + "rated_4 ,rated_3,rated_2 ,rated_1, top_voted_genre, top_voted_votes,2nd_voted_genre, " \
                  + "2nd_voted_votes, 3nd_voted_genre, 3nd_voted_votes) VALUES " \
                  + f"({book.link}, {book.top_of}, {book.name}, {book.author}, {book.rating.average_rating}, " \
                  + f"{book.rating.number_of_reviews}, "
        for i in range(5):
            command += f"{book.rating.rating_histogram[5-i]}, "
        for i in range(book.GENRE_NUM):
            command += f"{book.genres[i][0]}, "
            command += f"{book.genres[i][1]}, "
        command += ")"
        sql_run(connection, command)
    return True


def main():
    connection = establish_connection()
    save_top_genres(connection)
    save_books(connection)

if __name__=="__main__":
    main()