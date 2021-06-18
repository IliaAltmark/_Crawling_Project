from bs4 import BeautifulSoup
import requests
from crawler_prototype import DOMAIN
from selenium.webdriver.common.keys import Keys
from utils import quiet_selenium_chrome_driver


class BookRating:

    def __init__(self, rating_histogram, average_rating, number_of_ratings):
        self.average_rating = average_rating
        self.number_of_reviews = number_of_ratings
        self.rating_histogram = rating_histogram
        # TODO: assert that average_rating is indeed the average
        # TODO: assert that number of ratings is indeed number_of_ratings

    def __str__(self):
        return f"Rating information:\nAverage rating= {self.average_rating}\nNumber of reviews: {self.number_of_reviews}\nRating histogram:{self.rating_histogram}"


class Book:
    # TODO: describe genres and rating structure

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
        book._name_from_soup()
        book._genres_from_soup()
        book._author_from_soup()
        book._rating_from_soup()
        book._description_from_soup()
        if not to_save_soup:
            book.soup = None
        return book

    def soup_from_link(self):
        # runs chrome, browse to the link
        driver = quiet_selenium_chrome_driver()
        driver.get(self.link)

        # clicks on the rating_details button
        elem = driver.find_element_by_id('rating_details')
        elem.send_keys(Keys.RETURN)

        self.soup = BeautifulSoup(driver.page_source, features="lxml")
        driver.close()

        # user_agent = {'User-agent': 'Mozilla/5.0'}
        # response1 = requests.get(self.link, headers=user_agent)
        # self.soup = BeautifulSoup(response1.content, "html.parser")

    def _name_from_soup(self):
        if self.soup is None:
            self.soup_from_link()
        tag = self.soup.find("h1", attrs={"id": "bookTitle"})
        name = tag.text.strip()
        self.name = name

    def _author_from_soup(self):
        if self.soup is None:
            self.soup_from_link()
        tag = self.soup.find("a", attrs={"class": "authorName"})
        author = tag.text
        self.author = author

    def _description_from_soup(self):
        if self.soup is None:
            self.soup_from_link()
        tag = self.soup.find("div", attrs={"id": "description"})
        description = tag.text.strip()
        self.description = description

    def _rating_from_soup(self):
        if self.soup is None:
            self.soup_from_link()
        tag = self.soup.find("span", attrs={"itemprop": "ratingValue"})
        rating = float(tag.text.strip())
        tag2 = self.soup.find("meta", attrs={"itemprop": "ratingCount"})
        num_ratings = int(tag2.attrs["content"])
        rating_dist_tag = self.soup.find("table", attrs={"id": "rating_distribution"})
        tags3 = rating_dist_tag.findAll("tr", limit=5)
        rating_histogram = {}
        for i, tag3 in enumerate(tags3):
            rating_per_stars = tag3.findAll("td")[1].text.strip()
            rating_histogram[5 - i] = int(rating_per_stars[rating_per_stars.find("(") + 1: rating_per_stars.find(")")])
        self.rating = BookRating(average_rating=rating, number_of_ratings=num_ratings,
                                 rating_histogram=rating_histogram)

    def _genres_from_soup(self):
        if self.soup is None:
            self.soup_from_link()
        genres_dict = {}

        # Find all genres' user ratings
        genres_user_ratings = self.soup.findAll("div", attrs={"class": "greyText bookPageGenreLink"})
        # For each rating finds the corresponding genre
        for rating in genres_user_ratings:
            genre_tags = rating.parent.parent.findAll('a', attrs={'class': 'actionLinkLite bookPageGenreLink'})
            genre = tuple(map(lambda x: x.text, genre_tags))
            genres_dict[genre] = int(rating.text.strip().split(" ")[0].replace(",", ""))
        self.genres = genres_dict

    def __str__(self):
        return f"--------The Book: {self.name}--------" + "\n" + f"--------By:{self.author}\n\ndescription: {self.description}\n" \
                                                                 f"\nlink: {self.link}\nrating:{self.rating}\ngenre: {self.genres}"


def main():
    """
    Tests the books scraper
    """
    link = "https://www.goodreads.com/book/show/51792100-a-burning?from_choice=true,best-fiction-books-2020"
    book = Book.book_from_link(link)
    print(book)


if __name__ == "__main__":
    main()
