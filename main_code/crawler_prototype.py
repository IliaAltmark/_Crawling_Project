"""
Authors: Ilia Altmark and Tovi Benoni
First crawler
"""
from bs4 import BeautifulSoup
import requests

URL = "https://www.goodreads.com/choiceawards/best-books-2020"


def main():
    user_agent = {'User-agent': 'Mozilla/5.0'}
    response1 = requests.get(URL, headers=user_agent)

    soup1 = BeautifulSoup(response1.content, "html.parser")
    tag = soup1.find("div", attrs={"id": "categories"})

    links_to_pages = [t['href'] for t in tag.findAll("a")]
    links_to_pages = list(filter(lambda t: True if t != '#' else False,
                                 links_to_pages))

    print(links_to_pages)


if __name__ == "__main__":
    main()
