# Python Scraping Scripts
A repository for scraping scripts using Python.  This is part of an ongoing project to develop tools for text analytics on major online crowd-sourced business reviews platforms (Yelp, TripAdvisor, Google +, etc).

===
# Info  

## scrapeYelp.py:  
Tested on Python 3.5.1  
Dependencies: bs4 4.4.1, pandas 0.18.0

Scrapes user reviews and rating for any business in Yelp and copies a csv formated file to your current working directory. The script is meant to be run in the command line with arguments "your business url" and "name of file" in order with no extension for the file.  

Example: python3 scrapeYelp.py https://www.yelp.com/biz/king-kush-san-francisco-3 kkush_review_data  

## updateYelpReviews.py
Tested on Python 3.5.1  
Dependencies: bs4 4.4.1

This script updates an existing file containing Yelp review data that has been previously scraped with scrapeYelp.py. It is meant to be run in the command line with arguments "your business url" and "name of file to be updated" in order.   
Example: python3 scrapeYelp.py https://www.yelp.com/biz/king-kush-san-francisco-3 kkush_review_data.csv  