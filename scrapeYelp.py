# This script scrapes customer reviews and rating for a business in Yelp.  
# Copies a csv file to the current working directory.  
# Command line args: business Yelp url & name for output file w/o extension.  
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
    site = urllib.request.urlopen(link)
    soup = BeautifulSoup(site, 'lxml')
    rev_count = str(soup.find('span', class_ = "tab-link_count"))
    rev_count = re.findall(r'\d+', rev_count)[0]
    site.close()
    return(int(rev_count))


# Performs scraping. 
# Returns tuple containing lists of ratings and text for all reviews in a url.  
def scrape_yelp(link):
    site = urllib.request.urlopen(link)
    
    # Parsing site for reveiws and rating.  
    soup = BeautifulSoup(site, "lxml")
    reviews = soup.find_all('p', itemprop = "description")
    ratings = soup.find_all('meta', itemprop = "ratingValue")
    ratings = ratings[1:len(ratings)] # Position 0 is business overall rating.  
    
    # List of text with HTML and markup tags removed.   
    revs = [BeautifulSoup(str(review), 'lxml').get_text() for review in reviews]
    
    # List of rating values of type float.  
    rts = [float(re.findall('[0-9].[0-9]', str(rate))[0]) for rate in ratings]
    
    site.close()
    
    return(rts, revs)


# Obtaining business url from command line.  
business_url = sys.argv[1]

# Retrieve total number of reviews in the English language.     
review_count = get_review_count(business_url)

print("Scraping", review_count, "from Yelp business url:\n", "   "+business_url)

# Scraping business main page.  
business_review_rating = scrape_yelp(business_url)

# Scraping additional reviews pages if review count exceeds 20.  
# Yelp returns a max of 20 reviews per page.  
# Url is modified by adding ?start=20 to main url & increase number by 20.  
# Ranges from 20 to review count.
# Extends bussiness_review_rating with additional data.  

if review_count > 20:
    for number in range(20, review_count, 20):   
        new_url = business_url+"?start="+str(number)
        add_review_rating = scrape_yelp(new_url)
        business_review_rating[0].extend(add_review_rating[0])
        business_review_rating[1].extend(add_review_rating[1])

# Confirms number of reviews and ratings.  
print("Total number of ratings:", str(len(business_review_rating[0])))
print("Total number of reviews:", str(len(business_review_rating[1])))

# Create path and extension for output file.  
output_file_path = './'+sys.argv[2]+'.csv'

with open(output_file_path, 'w') as f:   
    # Configures writer to write standard csv file.  
    writer = csv.writer(f, delimiter=',', quotechar='"')
    writer.writerow(['rating', 'review'])
    # Writing rating and reviews to file.  
    for rt, rev in zip(business_review_rating[0], business_review_rating[1]):
        writer.writerow([rt, rev])

print('Copied file:', output_file_path)