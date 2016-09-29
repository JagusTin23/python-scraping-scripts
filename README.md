# python-scraping-scripts
A repository for scraping scripts using Python.  

===
# ScripT Info  

## scrapeYelp.py:  
Tested on Python 3.5.1  
Dependencies: bs4 4.4.1, pandas 0.18.0   

Scrapes user reviews and rating for any business in Yelp and copies a csv file to your current working directory. The script is meant to be run in the command line with arguments "your business url" and "name of file" in order with no extension for the file.  

Example: python3 scrapeYelp.py https://www.yelp.com/biz/king-kush-san-francisco-3 kkush_review_data  
