# Goodreads web scraper

The program extracts the information of the top 2020 books from the Goodreads website.

## Description

The Goodreads website gives various details on books, including a users based evaluation 
and genre determination. This program extracts from Goodreads information on the top 2020
books according to the website user-based evaluation.

For each book, the system extracts the following details:
  - Title
  - Author
  - Description
  - Genre (A dictionary of top voted generes with their number of votes)
  - Rating histogram (Number of voters per number of stars)

The program saves all the information in a csv file.

## Getting Started

### Dependencies

In order to use the program, the following python packages must be installed in 
the interpreter running the program:
  - beautifulsoup4 version 4.9.3
  - bs4 version 0.0.1
  - certifi version 2021.5.30
  - chardet version 4.0.0
  - idna version 2.10
  - requests version 2.25.1
  - soupsieve version 2.2.1
  - urllib3 version 1.26.5
  - selenium version 3.141.0 (with Chrome web driver)

### Installing

- The program can be run using any python interpreter satisfying the requirements 
described in the dependencies section. 
- A Chrome web driver executable must be placed in your path in order for selenium to work 
  (See https://selenium-python.readthedocs.io/installation.html#drivers for more details).

### Executing program

* How to run the program:
  
  The uploaded directory contains a number of scripts which are used without
  additional parameters. Contains the following scripts:
  * book_scraper.py - Can be used for testing and scraping specific links.
  * link_scraper.py - Scrapes links that contain book info. Currently, scrapes
    only the top books per genre but can be easily changed by manipulation of 
    the Beautiful Soup tags. For example:
    
    ``tag = soup("a", attrs={"class": "pollAnswer__bookLink"})``
  * save_to_csv.py - Uses the class Book for scraping from a list that contains 
    links to books. The scraped data is then saved to a csv
* Step-by-step bullets:
  * The first step is to use link_scraper.py which creates a csv that contains 
    links to books.
  * Next step is to use save_to_csv.py which will go over the specified csv
    file (the file created in the previous step) and then scrapes and saves 
    book data in a separate csv.

## Help

Any advice for common problems or issues:
* Make sure to not open the csv (where the data is written to) file when writing the scraped data.

## Authors

ex. Ilia Altmark

ex. Tovi Benoni

## Version History

Currently redundent

## License

Currently redundent

## Acknowledgments

TODO
