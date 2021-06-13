from bs4 import BeautifulSoup
import requests
from crawler_prototype import DOMAIN


class BookRating:

    def __init__(self, average_rating, number_of_reviews, rating_histogram):
        self.average_rating = average_rating
        self.number_of_reviews = number_of_reviews
        self.rating_histogram = rating_histogram
        # TODO: assert that average_rating is indeed the average


class Book:
    # TODO: describe genres and rating structure
    # TODO: write the rating and genres func

    def __init__(self, name, author, rating, genres, description, link, soup=None):
        self.name = name
        self.author = author
        self.rating = rating
        self.genres = genres
        self.description = description
        self.link = link
        self.soup = soup

    @classmethod
    def book_from_link(cls, link, to_save_soup=True):
        """
        Creates a book object from link
        :param to_save_soup: TODO
        :param link to the book's page
        :return: a book object
        """

    def soup_from_link(self):
        user_agent = {'User-agent': 'Mozilla/5.0'}
        response1 = requests.get(self.link, headers=user_agent)
        self.soup = BeautifulSoup(response1.content, "html.parser")

    def _name_from_link(self):
        if self.soup is None:
            self.soup_from_link()
        tag = self.soup.find("h1", attrs={"id": "bookTitle"})
        name = tag.text.strip()
        self.name = name

    def _author_from_link(self):
        if self.soup is None:
            self.soup_from_link()
        tag = self.soup.find("a", attrs={"class": "authorName"})
        author = tag.text
        self.author = author

    def _description_from_link(self):
        if self.soup is None:
            self.soup_from_link()
        tag = self.soup.find("div", attrs={"id": "description"})
        description = tag.text.strip()
        self.description = description
