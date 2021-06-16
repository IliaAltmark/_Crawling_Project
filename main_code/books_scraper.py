from bs4 import BeautifulSoup
import requests
from crawler_prototype import DOMAIN
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class BookRating:

    def __init__(self, rating_histogram, average_rating, number_of_ratings):
        self.average_rating = average_rating
        self.number_of_reviews = number_of_ratings
        self.rating_histogram = rating_histogram
        # TODO: assert that average_rating is indeed the average
        # TODO: assert that number of ratings is indeed number_of_ratungs


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
        book = Book(name=None, author=None, rating=None, genres=None, description=None, link=link, soup=None)
        book.soup_from_link()
        book._name_from_link()
        # book._genres_from_link()
        book._author_from_link()
        book._rating_from_link()
        book._description_from_link()
        return book

    def soup_from_link(self):
        # runs chrome, browse to the link
        driver = webdriver.Chrome()
        driver.get(self.link)

        # clicks on the rating_details button
        elem = driver.find_element_by_id('rating_details')
        elem.send_keys(Keys.RETURN)

        self.soup = BeautifulSoup(driver.page_source, features="lxml")
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
        rating = float(tag.text.strip())
        tag2 = self.soup.find("meta", attrs={"itemprop": "ratingCount"})
        num_ratings = int(tag2.attrs["content"])
        tags3 = tag.findAll("tr", limit=5)
        rating_histogram = {}
        for i, tag3 in enumerate(tags3):
            rating_per_stars = tag3.findAll("td")[1].text.strip()
            rating_histogram[5 - i] = int(rating_per_stars[rating_per_stars.find("(") + 1 : rating_per_stars.find(")")])
        self.rating = BookRating(average_rating=rating, number_of_ratings=num_ratings,
                                 rating_histogram=rating_histogram)

    """
    def _genres_from_link(self):
        if self.soup is None:
            self.soup_from_link()
        tag = self.soup.find("div", attrs={"class": "bigBoxContent containerWithHeaderContent"})
        genres_dict = {}
    """


def main():
    """
    Tests the books scraper
    """
    link = "https://www.goodreads.com/book/show/51231889-nobody-will-tell-you-this-but-me"
    book = Book.book_from_link(link)
    print(book)


if __name__ == "__main__":
    main()
