"""
Authors: Ilia Altmark and Tovi Benoni
First crawler
"""
import csv
from book_scraper import Book


# DOMAIN = "https://www.goodreads.com"
# URL = DOMAIN + "/choiceawards/best-books-2020"


def main():
    book_dict = {'name': [], 'author': [], 'description': [],
                 'average_rating': [], 'number_of_reviews': [],
                 'top_of': [],
                 'rated_5': [], 'rated_4': [], 'rated_3': [], 'rated_2': [],
                 'rated_1': [],
                 'top_voted_genre': [], 'top_voted_votes': [],
                 '2nd_voted_genre': [], '2nd_voted_votes': [],
                 '3rd_voted_genre': [], '3rd_voted_votes': []}

    with open('links_to_books.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)

        for i, row in enumerate(reader):
            # if i >= 70:
            #     break

            if 70 <= i < 120:

                print(f"Scraping row number {i}...")

                link = row[0]
                book = Book.book_from_link(link)
                book_dict['name'].append(
                    book.name)
                book_dict['author'].append(
                    book.author)
                book_dict['description'].append(
                    book.description)
                book_dict['average_rating'].append(
                    book.rating.average_rating)
                book_dict['number_of_reviews'].append(
                    book.rating.number_of_reviews)
                book_dict['top_of'].append(row[1])
                book_dict['rated_5'].append(
                    book.rating.rating_histogram[5])
                book_dict['rated_4'].append(
                    book.rating.rating_histogram[4])
                book_dict['rated_3'].append(
                    book.rating.rating_histogram[3])
                book_dict['rated_2'].append(
                    book.rating.rating_histogram[2])
                book_dict['rated_1'].append(
                    book.rating.rating_histogram[1])

                genres = iter(book.genres)

                top_voted_key = next(genres)
                book_dict['top_voted_genre'].append(top_voted_key[0])
                book_dict['top_voted_votes'].append(
                    book.genres[top_voted_key])

                second_voted_key = next(genres)
                book_dict['2nd_voted_genre'].append(second_voted_key[0])
                book_dict['2nd_voted_votes'].append(
                    book.genres[second_voted_key])

                third_voted_key = next(genres)
                book_dict['3rd_voted_genre'].append(third_voted_key[0])
                book_dict['3rd_voted_votes'].append(
                    book.genres[third_voted_key])

    with open('books_full.csv', 'w', newline='',
              encoding='utf-8') as csv_file:

        writer = csv.writer(csv_file)
        writer.writerow(book_dict.keys())
        writer.writerows(zip(*book_dict.values()))


if __name__ == "__main__":
    main()
