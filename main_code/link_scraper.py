"""
Authors: Ilia Altmark and Tovi Benoni
scrapes and saves links which contain book data for further scraping
"""
# imports from project files
from utils import USER_AGENT, DOMAIN, URL_GENRE, URL_TOP, \
    quiet_selenium_chrome_driver, LOGIN_PAGE, EMAIL, PASS

# imports from packages
from bs4 import BeautifulSoup as bs
import requests


def get_soup(link):
    """
    saves and parses the html and returns a BS object
    :param link: received link
    :return: BS object
    """
    response = requests.get(link, headers=USER_AGENT)
    return bs(response.content, "lxml")


def extract_links(url, class_tag, driver=None):
    """
    extracts the necessary links from given url and class tag
    """
    if driver:
        driver.get(url)
        soup = bs(driver.page_source, features="lxml")
    else:
        soup = get_soup(url)

    # finds the "a" tag with class=class_tag
    tag = soup("a", attrs={"class": class_tag})

    # extracts all the links from the tags
    links_to_books = [t['href'] for t in tag]
    links_to_books = [DOMAIN + link for link in links_to_books]

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


def site_login(driver):
    """
    logins to the website
    """
    driver.get(LOGIN_PAGE)
    driver.find_element_by_id("user_email").send_keys(EMAIL)
    driver.find_element_by_id("user_password").send_keys(PASS)
    driver.find_element_by_name("next").click()


def fills_links(driver, links, page_range, page, target_url, genre_url, genre):
    """
    fills links dict with links to books per page
    :param driver: received selenium driver
    :param links: link dictionary
    :param page_range: number of pages to scrape
    :param page: first page to scrape
    :param target_url: url to scrape
    :param genre_url: url of the genre
    :param genre: genre to scrape
    :return:
    """
    print(f"Scraping {genre} page...")

    for p in range(page_range):
        print(f"Scraping page {page}...")
        links_to_books = extract_links(target_url, "bookTitle", driver)
        links[None] += links_to_books

        if page:
            page += 1
            target_url = genre_url + f"?page={page}"


def get_links_to_books_genre(genre, page, to_page):
    """
    extracts links to specific books from a specific genre
    :param genre: the requested genre
    :param page: starting page
    :param to_page: last page
    """
    driver = quiet_selenium_chrome_driver()
    try:
        site_login(driver)
        genre_url = URL_GENRE + genre
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
        fills_links(driver, links, page_range, page, target_url, genre_url,
                    genre)
        return links

    finally:
        driver.close()


def get_links_to_top_genres():
    """
    goes to the predefined URL and extracts the links to the top books
    :return: a list containing the top books per genre
    """
    soup = get_soup(URL_TOP)

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
