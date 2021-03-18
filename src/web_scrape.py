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
  summaries = []
  tables = []
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
    summaries.append(summary)
    tables.append(summary_table)

  return summaries, tables



# %%

def scrape_data(url, url2, zipcodes, num_units):
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
  return sub_links


  # %%
  def scrape_details(url, subs):
    output = []
    for idx, s in enumerate(sub_links):
      d = {}
      print(s)
      new_link = url[:25] + str(s)

      req = urllib.request.Request(new_link, headers={'User-Agent' : 'Magic Browser'})
      response = urllib.request.urlopen( req )
      html = response.read()
      soup = BeautifulSoup(html, 'html.parser')

      name = soup.find('h1', class_ = "facility-name sf-type sf-type-large").get_text()
      name = name.split('-')[0]
      d['name'] = name

      address = soup.find('h2',  class_ = "facility-address sf-type").get_text()
      d['address'] = address

      city = soup.find('h2',  class_ = "facility-address sf-type").get_text()
      city = city.split(' ')[-3].strip(',')
      d['city'] = city

      state = soup.find('h2',  class_ = "facility-address sf-type").get_text()
      state = state.split(' ')[-2]
      d['state'] = state

      zipcode = soup.find('h2',  class_ = "facility-address sf-type").get_text()
      zipcode = zipcode.split(' ')[-1]
      d['zipcode'] = zipcode

      phone = soup.find('span', class_ = "number").get_text()
      d['phone'] = phone

      try:
        rating = soup.find('span', class_ = "sf-type sf-type-tiny").get_text()
        rating = rating.split(' ')[0]
      except AttributeError:
        rating = 'N/A'
      d['rating'] = rating

      try:
        reviews = soup.find('span' , class_ = "review-count sf-type").get_text()
        reviews = reviews.split(' ')[-2]
      except AttributeError:
        reviews = 'N/A'
      d['reviews'] = reviews

      amenities = soup.findAll('div', class_ = "amenity")
      for idx, i in enumerate(amenities):
        amm = i.get_text()
        if i.svg['class'][1] == 'checkmark':
          d[amm] = 1
        else:
          d[amm] = 0
      output.append(d)
    print(idx)
    time.sleep(random.randint(1,6))
    df = pd.DataFrame(output)
    return df



# %%




# %%

if __name__ == '__main__':
  zipcodes = []
  zipper =''
  while zipper != 'done':
    zipper = input("enter zip code or type 'done': ")

    if zipper != 'done':
      zipcodes.append(zipper)
    print(zipcodes)

  url = 'https://www.sparefoot.com/search.html?location='
  summaries, tables = get_summary(url, zipcodes)

  num_units = 20
  url2 = '&searchType=storage&page=1&listingsPerPage=' + str(num_units)

  sub_links = scrape_data(url, url2, zipcodes, num_units)

  df = scrape_details(url, sub_links)
  print(df.head())



# %%

df.head()
# %%
