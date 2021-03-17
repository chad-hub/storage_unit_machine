# %%
from pymongo import MongoClient
import pprint
from bs4 import BeautifulSoup
import requests
import time
import random
import selenium
import urllib.request

import pandas as pd
# %%
def get_summary(url, zipcodes):
  for z in zipcodes:
    sub_links = []
    search_url = url + str(z)
    req = urllib.request.Request(search_url, headers={'User-Agent' : 'Magic Browser'})
    response = urllib.request.urlopen( req )
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    num_entries = soup.find('span', class_ = "pagination-summary strong family-standard ph-text").text
    summary = num_entries[10:]
    n = int(summary[:3])
    summary_table = pd.read_html(search_url)
    print(summary)
    print(summary_table[0].head())

    return n, summary_table



# %%

def scrape_data(url, url2, zipcodes, num_units):
  # searches = []
  for z in zipcodes:
    sub_links = []
    search_url = url + str(z) + url2
    req = urllib.request.Request(search_url, headers={'User-Agent' : 'Magic Browser'})
    response = urllib.request.urlopen( req )
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    test = soup.findAll('a', class_ = "hide-border ph-link")
    for i in test:
      link = i.get('href')
      sub_links.append(link)
  sub_links = sub_links[2:num_units+2]
  for s in sub_links:
    new_link = url[:26] + s
    sub_req = urllib.request.Request(new_link, headers={'User-Agent' : 'Magic Browser'})
    sub_response = urllib.request.urlopen( sub_req )
    sub_html = sub_response.read()
    sub_soup = BeautifulSoup(sub_html, 'html.parser')


  # searches.append(sub_links)

  print(len(sub_links))
  for i in sub_links:
    print(i)





# %%

if __name__ == '__main__':
  zipcode = [int(input('Enter zip code:'))]
  url = 'https://www.sparefoot.com/search.html?location='
  num_units, table = get_summary(url, zipcode)
  if num_units > 100:
    num_units = 100

  url2 = '&searchType=storage&page=1&listingsPerPage=' + str(num_units)
  table
  # scrape_data(url, url2, zipcode, num_units)


# %%


# %%
