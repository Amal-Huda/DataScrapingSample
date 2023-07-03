# importing necessary libraries
import re
import time
import random
import asyncio
import pandas as pd
from datetime import datetime
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup, ResultSet
import requests
# Request to website and download HTML contents

payload={}
pdt_names = []
pdt_links=[]
pdt_urls=[]
pdt_ratings=[]
pdt_capacities=[]
pdt_saleprice=[]
pdt_mrp=[]
pdt_type=[]
pdt_reviews=[]
pdt_starrting=[]

for i in range(1,8):
    url = 'https://www.flipkart.com/microwave-ovens/pr?sid=j9e%2Cm38%2Co49&page=' + str(i)

    print('page'+str(i))

    req=requests.get(url)
    content=req.text
    #print(content)
    soup=BeautifulSoup(content,'lxml')
    #print(soup)
    names = soup.find_all("div",class_="_4rR01T")
    links = soup.find_all("a", class_="_1fQZEK")
    #print(links)
    pdt_urls.append([link['href'] for link in links])

    ratings=soup.find_all("span",class_="_2_R_DZ")
    capacities=soup.find_all("li", class_="_21lJbe")
    controltypes=soup.find_all("li", class_="rgWa7D")
    reviews=soup.find_all("span")
    starrating=soup.find_all("div",class_="_3LWZlK")
    for review in reviews:
        if 'Reviews' in review.text :
            if 'Ratings' not in review.text:
                if '&' not in review.text:
                    if review is not None:

                        review=review.text.strip()
                        review=str(review).replace(',','')
                        pdt_reviews.append(review)


    #for r in pdt_reviews:

    for starrtng in starrating:
        pdt_starrting.append(starrtng.text)

    saleprices=soup.find_all("div",class_="_30jeq3 UMT9wN")
    saleprices2=soup.find_all("div",class_="_30jeq3 _1_WHN1")
    mrps=soup.find_all("div",class_="_3I9_wc _27UcVY")
    for cntrltype in controltypes:
        if "Control Type" in cntrltype.text:
            cntrltype = cntrltype.text.replace("Control Type:", "").strip()
            pdt_type.append(cntrltype)

    for mrp in mrps:
        pdt_mrp.append(mrp.text.replace("₹",""))


    #for saleprice in saleprices:
   # pdt_saleprice.append(saleprice.text)
    for saleprice in saleprices2:
        pdt_saleprice.append(saleprice.text.replace("₹",""))

    for name in names:
        pdt_names.append(name.text)


    for name in pdt_names:
        match = re.search(r'\b(\d+\s?L)\b', name)
        if match:
            extracted_value = match.group()
            #print(extracted_value)
            pdt_capacities.append(extracted_value)
    for rating in ratings:
        pdt_ratings.append(rating.text)
print("pdt_reviews")
print("links")
print(pdt_urls)
print(len(list(pdt_urls)))
print(pdt_starrting)
print(len(pdt_starrting))
print("pdt_type")
    #for t in pdt_type:

print(pdt_type)
print(len(pdt_type))
print("MRPS")
print(pdt_mrp)
print(len(pdt_mrp))
print("SALES PRICES")
print(pdt_saleprice)
print(len(pdt_saleprice))
print("product_names")
print(pdt_names)
print(len(pdt_names))
print("pdt_ratings")
print(pdt_ratings)
print(len(pdt_ratings))
    #for capa in capacities:
    #   pdt_capacities.append(capa.text)
print("pdt_capacities....")
print(pdt_capacities)
print(len(pdt_capacities))
print(pdt_reviews)
print(len(pdt_reviews))

df = pd.DataFrame({
    "Product URL":pdt_urls,
    "Product Title": pdt_names,
    #"Ratings and Reviews":pdt_ratings,
    #"Brand":,
    #"StarRating":pdt_starrting,
    #"Seller name":,
    "MRP":pdt_mrp,
    "Sale_price":pdt_saleprice,
    #"Model":,
    "Capacity":pdt_capacities,
    "Control Type":pdt_type,

    # Add other columns here
    })
print("df")
df.to_csv("scraped_data_multiplepages_flipkart.csv", index=False)
df_no_duplicates = df.drop_duplicates(subset=[ "pdt_urls",
    "pdt_names","pdt_mrp","pdt_saleprice","pdt_capacities","pdt_ype"])
df.to_csv("scraped_data_multiplepages_flipkart.csv", index=False)
print(df.head(10))