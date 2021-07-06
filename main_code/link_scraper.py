"""
Authors: Ilia Altmark and Tovi Benoni
scrapes and saves links which contain book data for further scraping
"""
# imports from project files
import utils as u

# imports from packages
from bs4 import BeautifulSoup
import requests


def get_soup(link):
    """
    saves and parses the html and returns a BS object
    :param link: received link
    :return: BS object
    """
    response = requests.get(link, headers=u.USER_AGENT)
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
        links_to_books = [u.DOMAIN + link for link in links_to_books]

        links_per_genre[genre] = links_to_books

    return links_per_genre


def get_links_to_books_genre(genre, page):
    pass
    # links_per_genre = {}
    #
    # for link in links:
    #     genre = link.split('/')[-1]
    #     print(f"Scraping {genre} page...")
    #
    #     soup = get_soup(link)
    #
    #     # finds the "a" tag with class="pollAnswer__bookLink"
    #     tag = soup("a", attrs={"class": "pollAnswer__bookLink"})
    #
    #     # extracts all the links from the tags
    #     links_to_books = [t['href'] for t in tag]
    #     links_to_books = [u.DOMAIN + link for link in links_to_books]
    #
    #     links_per_genre[genre] = links_to_books
    #
    # return links_per_genre


def get_links_to_top_genres():
    """
    goes to the predefined URL and extracts the links to the top books
    :return: a list containing the top books per genre
    """
    soup = get_soup(u.URL_TOP)

    # finds the div with id="categories"
    tag = soup.find("div", attrs={"id": "categories"})

    # extracts all the links from the div
    links_to_pages = [t['href'] for t in tag.findAll("a")]

    # cleaning empty links
    links_to_pages = list(filter(lambda link: True if link != '#' else False,
                                 links_to_pages))

    # turning into actual links and not dirs
    links_to_pages = [u.DOMAIN + link for link in links_to_pages]

    return links_to_pages
