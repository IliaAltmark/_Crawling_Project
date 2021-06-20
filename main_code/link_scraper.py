"""
Authors: Ilia Altmark and Tovi Benoni
First crawler
"""
import csv

from bs4 import BeautifulSoup
import requests

DOMAIN = "https://www.goodreads.com"
URL = DOMAIN + "/choiceawards/best-books-2020"
USER_AGENT = {'User-agent': 'Mozilla/5.0'}


def get_soup(link):
    response = requests.get(link, headers=USER_AGENT)
    return BeautifulSoup(response.content, "html.parser")


def get_link_to_books(links):
    """
    extracts links to specific books from the given list of pages
    :param links: a list containing pages of top books per genre
    :return: dictionary where key is genre and value is a list of books
    """

    links_per_genre = {}

    for link in links:
        genre = link.split('/')[-1]
        print(f"Scraping {genre} page...")

        soup = get_soup(link)

        # finds the "a" tag with class="pollAnswer__bookLink"
        tag = soup("a", attrs={"class": "pollAnswer__bookLink"})

        # extracts all the links from the tags
        links_to_books = [t['href'] for t in tag]
        links_to_books = [DOMAIN + link for link in links_to_books]

        links_per_genre[genre] = links_to_books

    return links_per_genre


def get_links_to_top_genres():
    """
    goes to the predefined URL and extracts the links to the top books
    :return: a list containing the top books per genre
    """
    soup = get_soup(URL)

    # finds the div with id="categories"
    tag = soup.find("div", attrs={"id": "categories"})

    # extracts all the links from the div
    links_to_pages = [t['href'] for t in tag.findAll("a")]

    # cleaning empty links
    links_to_pages = list(filter(lambda link: True if link != '#' else False,
                                 links_to_pages))

    # turning into actual links and not dirs
    links_to_pages = [DOMAIN + link for link in links_to_pages]

    return links_to_pages


def main():
    links_to_top_genres = get_links_to_top_genres()

    links_to_top_books = get_link_to_books(links_to_top_genres)

    with open('../project_data/links_to_books.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        for genre, books in links_to_top_books.items():
            print(f"Links for {genre}:")

            for book in books:
                writer.writerow([book, genre])
                print(book)


if __name__ == "__main__":
    main()
