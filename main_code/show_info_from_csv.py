"""
Authors: Ilia Altmark and Tovi Benoni
First crawler
"""
import csv
from books_scraper import Book

DOMAIN = "https://www.goodreads.com"
URL = DOMAIN + "/choiceawards/best-books-2020"


def main():
    book_dict = {'name': [], 'author': [], 'description': [],
                 'average_rating': [], 'number_of_reviews': [], 'top_of': []}

    with open('links_to_books.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)

        for i, row in enumerate(reader):
            print(f"Printing row number {i}...")
            if i >= 1:
                break

            link = row[0]
            book = Book.book_from_link(link)
            book_dict['name'].append(
                book.name.encode("utf-8", errors='replace'))
            book_dict['author'].append(
                book.author.encode("utf-8", errors='replace'))
            book_dict['description'].append(
                book.description.encode("utf-8", errors='replace'))
            book_dict['average_rating'].append(
                book.rating.average_rating)
            book_dict['number_of_reviews'].append(
                book.rating.number_of_reviews)
            book_dict['top_of'].append(row[1])

    with open('books.csv', 'w', newline='') as csv_file:

        writer = csv.writer(csv_file)
        writer.writerow(book_dict.keys())
        writer.writerows(zip(*book_dict.values()))


if __name__ == "__main__":
    main()
