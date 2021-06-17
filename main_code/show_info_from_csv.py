"""
Authors: Ilia Altmark and Tovi Benoni
First crawler
"""
import csv
from books_scraper import Book

DOMAIN = "https://www.goodreads.com"
URL = DOMAIN + "/choiceawards/best-books-2020"


def main():
    with open('links_to_books.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            link = row[0]
            book = Book.book_from_link(link)
            print(book)


if __name__ == "__main__":
    main()
