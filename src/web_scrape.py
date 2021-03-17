# %%
from pymongo import MongoClient
import pprint
from bs4 import BeautifulSoup
import requests
import time
import random
import selenium
import urllib.request
# %%
def scrape_data(url, url2, zipcodes):
  sub_links = []
  for z in zipcodes:
    search_url = url + str(z) + url2
    req = urllib.request.Request(search_url, headers={'User-Agent' : 'Magic Browser'})
    response = urllib.request.urlopen( req )
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    test = soup.findAll('a', class_ = "hide-border ph-link")
    for i in test:
      link = i.get('href')
      sub_links.append(link)
  sub_links = sub_links[2:102]
  # for idx,i in enumerate(sub_links):
  #   # print(type(i[-4:]))
  #   try:
  #     if i[-4:] != 'html':
  #       sub_links.remove(i)
  #   except TypeError:
  #     sub_links.remove(i)
  print(len(sub_links))
  for i in sub_links:
    print(i)









# %%

if __name__ == '__main__':
  num_units = 150
  url = 'https://www.sparefoot.com/search.html?location='
  url2 = '&searchType=storage&page=1&listingsPerPage=' + str(num_units)


  scrape_data(url, url2, [78701])

# %%


# %%
