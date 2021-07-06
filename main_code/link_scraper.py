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


def extract_links(url, class_tag):
    """
    extracts the necessary links from given url and class tag
    """
    soup = get_soup(url)

    # finds the "a" tag with class=class_tag
    tag = soup("a", attrs={"class": class_tag})

    # extracts all the links from the tags
    links_to_books = [t['href'] for t in tag]
    links_to_books = [u.DOMAIN + link for link in links_to_books]

    return links_to_books


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

        links_to_books = extract_links(link, "pollAnswer__bookLink")
        links_per_genre[genre] = links_to_books

    return links_per_genre


def get_links_to_books_genre(genre, page, to_page):
    """
    extracts links to specific books from a specific genre
    :param genre: the requested genre
    :param page: starting page
    :param to_page: last page
    """
    genre_url = u.URL_GENRE + genre
    if page:
        target_url = genre_url + f"?page={page}"
    else:
        target_url = genre_url

    page_range = 1
    if page and to_page:
        if (to_page - page) >= 1:
            page_range += to_page - page
        else:
            print('to_page must be bigger than page! '
                  'Now scraping only the first page.')

    links = {None: []}
    print(f"Scraping {genre} page...")

    for p in range(page_range):
        print(f"Scraping page {page}...")
        links_to_books = extract_links(target_url, "bookTitle")
        links[None] += links_to_books

        if page:
            page += 1
            target_url = genre_url + f"?page={page}"

    return links


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
