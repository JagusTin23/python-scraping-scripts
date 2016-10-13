# Appends an existing csv file with Yelp review data.
# Is meant to be used on a file that was created using scrapeYelp.py
# Command line args: business main Yelp url & name of file to be updated. 
# Built on Python 3.5.1

import sys
import re
import csv
import urllib.request
from bs4 import BeautifulSoup

# Verifies number of arguments in command line is correct.  
if len(sys.argv) != 3:
    sys.exit('Incorrect number of arguments passed in command line.')

# Retrieves number of reviews in English for a business in Yelp.  
def get_review_count(link):
    with urllib.request.urlopen(link) as site:
        soup = BeautifulSoup(site, 'lxml')
        rev_count = str(soup.find('span', class_ = 'tab-link_count'))
        rev_count = re.findall(r'\d+', rev_count)[0]
    return(int(rev_count))

# Performs scraping. 
# Returns tuple containing lists of ratings and text for all reviews in a url.   
def scrape_yelp(link):
    with urllib.request.urlopen(link) as site:
        # Parsing site for reveiws and rating.  
        soup = BeautifulSoup(site, 'lxml')
        reviews = soup.find_all('p', itemprop = 'description')
        ratings = soup.find_all('meta', itemprop = 'ratingValue')
        ratings = ratings[1:len(ratings)] # Position 0 is business rating.  
        # List of text with HTML and markup tags removed.   
        revs = [BeautifulSoup(str(_), 'lxml').get_text() for _ in reviews]
        # List of rating values of type int.  
        rts = [int(re.findall('[0-9]', str(_))[0]) for _ in ratings]
    return(rts, revs)

business_url = sys.argv[1]
file_to_update = sys.argv[2]
review_count = get_review_count(business_url)

# Retrieves number of reviews in file.  
with open(file_to_update) as f: 
    revsInFile = (sum(1 for line in f))

# Verifies if update is needed.  
if revsInFile == review_count:
    sys.exit('File is up to date.')

# Scrapping additional reviews if needed.  
if revsInFile < review_count:
    
    # Number of reviews to be updated.  
    revs_needed = review_count - revsInFile
    
    print('Scraping', revs_needed, 'reviews...')

    # Scraping main page. 
    business_review_rating = scrape_yelp(business_url)
    
    # Yelp restricts 20 reveiws per url.   
    # If reviews needed > than 20, then ?start=20 is added URL.  
    # Number is increased by 20 until all reviews are retrieve.   
    if revs_needed > 20:

        for number in range(20, revs_needed + 1, 20):   
            new_url = business_url+'?start='+str(number)
            add_review_rating = scrape_yelp(new_url)
            business_review_rating[0].extend(add_review_rating[0])
            business_review_rating[1].extend(add_review_rating[1])

# Get only reviews needed and reverses order for appending to csv file.   
missing_ratgs = business_review_rating[0][:revs_needed][::-1]
missing_revs = business_review_rating[1][:revs_needed][::-1]

# Appends csv file with reviews and ratings.  
with open(file_to_update, 'a') as outCSV:
    print('Updating', file_to_update, 'with', revs_needed, 'reviews..')
    writer = csv.writer(outCSV, delimiter=',', quoting = csv.QUOTE_NONNUMERIC)
    for ratg, rev in zip(missing_ratgs, missing_revs):
        writer.writerow([ratg, rev])
  
print('Update completed.')