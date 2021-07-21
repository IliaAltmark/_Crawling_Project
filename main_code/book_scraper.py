"""
Authors: Ilia Altmark and Tovi Benoni
Contains the Book class which is used for scraping the required data from a
link containing book data
"""
# imports from project files
from API_key import API_KEY
from utils import quiet_selenium_chrome_driver, USER_AGENT

# imports from packages
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import json
import requests


class BookRating:
    """
    A class for storing and manipulating a book's ratings data.
    The book's rating object consists of three attributes:
    average rating, number of ratings and rating histogram
    which shows how many people gave each score (1-5) to the book.
    """

    def __init__(self, rating_histogram, average_rating, number_of_ratings):
        self.average_rating = average_rating
        self.number_of_reviews = number_of_ratings
        self.rating_histogram = rating_histogram

    def __str__(self):
        return f"""Rating information:\nAverage rating= {self.average_rating}\n
               Number of reviews: {self.number_of_reviews}\n
               Rating histogram:{self.rating_histogram}"""


class Book:
    """
    A class for storing and manipulating a book's data
    """
    GENRE_NUM = 3

    def __init__(self, name, author, rating, genres, description, link,
                 published_date, page_count, soup=None):
        self.name = name
        self.author = author
        self.rating = rating
        self.genres = genres
        self.description = description
        self.link = link
        self.soup = soup
        self.published_date = published_date
        self.page_count = page_count

    @classmethod
    def book_from_link(cls, link, web_driver=None,
                       to_save_soup=True):
        """
        Creates a book object from link
        :param web_driver: a web driver to get the link's source code with.
        :param to_save_soup: defaults to True
        :param link: link to the book's page
        :return: a Book object
        :TODO change callings to include top_of
        """
        book = Book(name=None, author=None, rating=None, genres=None,
                    description=None, link=link, published_date=None,
                    page_count=None, soup=None)
        book.soup_from_link(web_driver=web_driver)
        book._name_from_soup()
        book._genres_from_soup()
        book._author_from_soup()
        book._rating_from_soup()
        book._description_from_soup()
        book._from_api()
        if not to_save_soup:
            book.soup = None
        return book

    def check_soup(self):
        """
        Checks if self.soup is None and if so derives self.soup_from_link
        """
        if self.soup is None:
            self.soup_from_link()

    def soup_from_link(self, web_driver=None, timeout=30):
        """
        Initializes self.soup from self.link
        :param web_driver: a web driver to get the link's source code with.
        :param timeout: the maximum time to wait for self.link to loud.
        """
        # runs chrome, browse to the link
        if not web_driver:
            driver = quiet_selenium_chrome_driver()
        else:
            driver = web_driver

        try:
            driver.get(self.link)

            # clicks on the rating_details button
            elem = WebDriverWait(driver, timeout).until(
                ec.presence_of_element_located(
                    locator=(By.ID, 'rating_details')))
            elem.send_keys(Keys.RETURN)

            self.soup = BeautifulSoup(driver.page_source, features="lxml")
        except TimeoutException:
            raise TimeoutException(
                f"Unable to load book. Either the link {self.link} "
                f"is wrong or the page took "
                f"too much time to load")
        finally:
            if not web_driver:
                driver.close()

    def _name_from_soup(self):
        """
        Initializes self.name from self.soup
        """
        self.check_soup()
        tag = self.soup.find("h1", attrs={"id": "bookTitle"})
        name = tag.text.strip()
        self.name = name

    def _author_from_soup(self):
        """
        Initializes self.author from self.soup
        """
        self.check_soup()
        tag = self.soup.find("a", attrs={"class": "authorName"})
        author = tag.text
        self.author = author

    def _description_from_soup(self):
        """
        Initializes self.description from self.soup
        """
        self.check_soup()
        tag = self.soup.find("div", attrs={"id": "description"})

        try:
            tag = tag("span")[1]
        except IndexError:
            pass

        description = tag.text.strip()
        self.description = description

    def _rating_from_soup(self):
        """
        Initializes self.rating from self.soup
        """
        self.check_soup()

        # finds the rating_average value
        rating_value_tag = self.soup.find("span",
                                          attrs={"itemprop": "ratingValue"})
        rating = float(rating_value_tag.text.strip())

        # finds the number of ratings value
        rating_count_tag = self.soup.find("meta",
                                          attrs={"itemprop": "ratingCount"})
        num_ratings = int(rating_count_tag.attrs["content"])

        # finds the rating histogram
        rating_dist_tag = self.soup.find("table",
                                         attrs={"id": "rating_distribution"})
        rating_stars_tag = rating_dist_tag.findAll("tr", limit=5)
        rating_histogram = {}
        for i, star_tag in enumerate(rating_stars_tag):
            # for each number of stars extracts the numbers of voters
            rating_per_stars = star_tag.findAll("td")[1].text.strip()
            rating_histogram[5 - i] = int(rating_per_stars[
                                          rating_per_stars.find(
                                              "(") + 1: rating_per_stars.find(
                                              ")")])
        self.rating = BookRating(average_rating=rating,
                                 number_of_ratings=num_ratings,
                                 rating_histogram=rating_histogram)

    def _genres_from_soup(self):
        """
        Initializes self.genres from self.soup.
        The genre attribute is a dictionary with genres as keys
        and users vote about what genre fits the book as values.
        """
        self.check_soup()
        genres_dict = {}

        # Find all genres' user ratings
        genres_user_ratings = self.soup.findAll("div", attrs={
            "class": "greyText bookPageGenreLink"})

        # For each rating finds the corresponding genre
        for rating in genres_user_ratings:
            genre_tags = rating.parent.parent.findAll('a', attrs={
                'class': 'actionLinkLite bookPageGenreLink'})
            genre = tuple(map(lambda x: x.text, genre_tags))
            genres_dict[genre] = int(
                rating.text.strip().split(" ")[0].replace(",", ""))
        self.genres = genres_dict

    def _from_api(self):
        search_title = self.name.lower()
        response = requests.get(
            f'''https://www.googleapis.com/books/v1/volumes?q=
                    {search_title}&key={API_KEY}''', headers=USER_AGENT)

        response_j = response.content.decode("utf-8")
        response_d = json.loads(response_j)
        first_book = response_d['items'][0]['volumeInfo']
        title = first_book['title'].lower()
        if search_title in title:
            try:
                published_date = first_book['publishedDate']
            except KeyError:
                published_date = None
            try:
                page_count = first_book['pageCount']
            except KeyError:
                page_count = None
        else:
            published_date = None
            page_count = None

        self.published_date = published_date
        self.page_count = page_count

    def __str__(self):
        return f"-------------------------------------------------------" \
               f"-----------\nThe Book:{self.name}\n" \
               f"--------------------------------------------------------" \
               f"----------" \
               + "\n" + f"--------By:{self.author}\n\ndescription: " \
                        f"{self.description}\n" \
                        f"\nlink: {self.link}\nrating:{self.rating}\n" \
                        f"genre: {self.genres}"
