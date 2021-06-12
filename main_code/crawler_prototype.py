"""
Authors: Ilia Altmark and Tovi Benoni
First crawler
"""
from bs4 import BeautifulSoup
import requests

DOMAIN = "https://www.goodreads.com"
URL = DOMAIN + "/choiceawards/best-books-2020"


def get_links_to_top_genres():
    """
    goes to the predefined URL and extracts the links to the top books
    :return: a list containing the top books per genre
    """
    user_agent = {'User-agent': 'Mozilla/5.0'}
    response1 = requests.get(URL, headers=user_agent)

    soup1 = BeautifulSoup(response1.content, "html.parser")

    # finds the div with id="categories"
    tag = soup1.find("div", attrs={"id": "categories"})

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

    for link in links_to_top_genres:
        print(link)


if __name__ == "__main__":
    main()
