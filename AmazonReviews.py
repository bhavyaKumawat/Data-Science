import requests
from bs4 import BeautifulSoup
import pandas as pd

data = pd.DataFrame()

link = "https://www.amazon.in/Test-Exclusive-747/product-reviews/B07DJCVTDN/ref=cm_cr_getr_d_paging_btm_next_{}?ie=UTF8&filterByStar=five_star&pageNumber={}&reviewerType=all_reviews"
pages = 100
for page in range(1, pages+1 , 1):
    amazon = link.format(page , page)
    respond = requests.get(amazon)    
    if (respond.status_code == 200):
        document = respond.content
        soup = BeautifulSoup(document , features="lxml")
        reviewlist = soup.find_all(attrs= {"data-hook": "review"})
        for review in reviewlist:
            children = review.div.div.contents
            _date = children[2].string
            _photo = children[0].find('noscript').img["src"]
            _name = (children[0].find('span')).string
            _rating = children[1].find(attrs= {"data-hook": "review-star-rating"}).string[:4]
            _review = children[4].find(attrs= {"data-hook": "review-body"}).span.string
            
            dataframe = pd.DataFrame({"Date": _date  , "Photo":_photo , "Name": _name , "Rating":_rating , "Review": _review} , index=[0]) 
            data = data.append(dataframe)
        
    
data.to_csv('amazon.csv' ,index=False)
