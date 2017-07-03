#!/usr/bin/env python
# -*- coding: utf-8 -*-
# urlib2 module is imported
import urllib2
# BeautifulSoup is used for web scraping pages
from bs4 import BeautifulSoup
#csv(comma separated values) used for spreadsheets,etc
import csv
from datetime import datetime

quote_page = [‘http://www.bloomberg.com/quote/SPX:IND', ‘https://www.bloomberg.com/quote/CCMP:IND']
data =[]
for pg in quote_page:
	page =urllib2.urlopen(pg)
	# html.parser for parsing text files formatted in html
	soup = BeautifulSoup(page, 'html.parser')

# strip() is used to remove starting and trailing
	name_box = soup.find('h1', attrs={'class': 'name'})
	name = name_box.text.strip()

# get the index price 
	price_box = soup.find('div', attrs={'class':'price'})
	price = price_box.text

# save the data in tuple
	data.append((name, price))
with open('index.csv', 'a') as csv_file:
	writer = csv.writer(csv_file)
	for name, price in data:
		writer.writerow([name, price, datetime.now()])
