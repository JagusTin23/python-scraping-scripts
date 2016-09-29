# This script scrapes customer reviews and rating for a business in Yelp.  
# Copies a csv file to the current working directory.  
# Command line args: business Yelp url & name for output file w/o extension.  
# Built on Python 3.5.1

import sys
import re
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup

# Verifies number of arguments in command line is correct.  
if len(sys.argv) != 3:
    sys.exit('Incorrect number of arguments passed in command line.')

# Retrieves number of reviews in English for a business in Yelp.  
def get_review_count(link):
    site = urllib.request.urlopen(link)
    soup = BeautifulSoup(site, 'lxml')
    rev_count = str(soup.find('span', itemprop = 'reviewCount'))
    rev_count = re.findall(r'\d+', rev_count)[0]
    site.close()
    return(int(rev_count))


# Performs scraping. 
# Returns tuple of rating and text per customer review.  
def scrape_yelp(link):
    site = urllib.request.urlopen(link)
    
    # Parsing site for reveiws and rating.  
    soup = BeautifulSoup(site, "lxml")
    reviews = soup.find_all('p', itemprop = "description")
    ratings = soup.find_all('meta', itemprop = "ratingValue")
    ratings = ratings[1:len(ratings)] # Position 0 is business overall rating.  
    
    review_lst = []  
    
    # Remove HTML tags from parsed reviews.  
    # Appends review_lst with plain text.  
    for review in reviews: 
        review = BeautifulSoup(str(review), 'lxml').get_text()
        review_lst.append(review)
    
    rating_lst = [] 
    
    # Obtain numeric value from parsed rating.
    # Appends rating_lst with rating value of type float.  
    for rating in ratings:
        rating = float(re.findall('[0-9].[0-9]', str(rating))[0])
        rating_lst.append(rating)
    
    site.close()
    
    return(zip(rating_lst, review_lst))

# Obtaining business url from command line.  
business_url = sys.argv[1]

# Retrieve total number of reviews.  
review_count = get_review_count(business_url)

# To appdend with scrape_yelp output.  
all_ratings = []
all_reviews = []

print("Scraping Yelp business:", business_url)

# Scraping business main page.  
main_business_review_rating = scrape_yelp(business_url)

# Appending all_reviews and all_ratings w/ main page reviews and ratings.  
for rating, review in main_business_review_rating:
    all_ratings.append(rating)
    all_reviews.append(review)

# Scraping additional business's reviews.  
# Yelp returns a max of 20 reviews per page.  
# Url is modified by adding ?start=20 to main url & increase number by 20.  
# Ranges from 20 to review count.  
for number in range(20, review_count, 20):   
    new_url = business_url+"?start="+str(number)
    review_rating = scrape_yelp(new_url)
    
    for rating, review in review_rating:
        all_ratings.append(rating)
        all_reviews.append(review)

# Verify total review/rating are equal.  
print("Total number of reviews:", str(len(all_reviews)))
print("Total number of ratings:", str(len(all_ratings)))

# Create pandas data frame with rating and review as columns.  
review_data = pd.DataFrame({'rating': all_ratings, 'review': all_reviews})

# Create path and extension for output file.  
output_file_path = './'+sys.argv[2]+'.csv'

# Output data to csv formatted file.  
review_data.to_csv(output_file_path, index=False)

print('Copied file:', output_file_path)

