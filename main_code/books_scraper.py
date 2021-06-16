from bs4 import BeautifulSoup
import requests
from crawler_prototype import DOMAIN
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class BookRating:

    def __init__(self, average_rating, number_of_ratings):
        self.average_rating = average_rating
        self.number_of_reviews = number_of_ratings
        # TODO:add histogram
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
        # runs chrome, browse to the link
        driver = webdriver.Chrome()
        driver.get(self.link)

        # clicks on the rating_details button
        elem = driver.find_element_by_id('rating_details')
        elem.send_keys(Keys.RETURN)

        self.soup = BeautifulSoup(driver.page_source)
        driver.close()


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

    def _rating_from_link(self):
        if self.soup is None:
            self.soup_from_link()
        tag = self.soup.find("span", attrs={"itemprop": "ratingValue"})
        rating = int(tag.text.strip())
        tag2 = self.soup.find("meta", attrs={"itemprop": "ratingCount"})
        num_ratings = int(tag2.attrs["content"])
        self.rating=BookRating(average_rating=rating,number_of_ratings=num_ratings)

    def _genres_from_link(self):
        if self.soup is None:
            self.soup_from_link()
        tag = self.soup.find("div", attrs={"class": "bigBoxContent containerWithHeaderContent"})
        genres_dict={}

