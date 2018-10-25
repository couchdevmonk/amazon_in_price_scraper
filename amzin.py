#Insipered from the blog: https://www.promptcloud.com/blog/tutorial-how-to-scrape-amazon-product-details-prices-using-python
#But I changed the code to suit my needs.

#import all the required modules
import re
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys
import warnings
from requests_html import HTMLSession

#declare a session object
session = HTMLSession()

#ignore warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")

url_array=[] #array for urls
asin_array=[] #array for asin numbers
with open('asin_list.csv', 'r') as csvfile:
    asin_reader = csv.reader(csvfile,delimiter=',')
    for row in asin_reader:
        asin_array.append(row[0]) #This url list is an array containing all the urls from the excel sheet
        print(asin_array)
#The ASIN Number will be between the dp/ and another /
start = 'dp/'
end = '/'
#for url in url_array:
#    asin_array.append(url[url.find(start)+len(start):url.rfind(end)]) #this array has all the asin numbers

#declare the header.
headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }

all_items=[] #The final 2D list containing prices and details of products, that will be converted to a consumable csv

for asin in asin_array:
    item_array=[] #An array to store details of a single product.
    #print(asin)
    amazon_url="https://www.amazon.in/dp/"+asin #The general structure of a url
    response = session.get(amazon_url, headers=headers, verify=False) #get the response
    #print(response.text)

#    item_array.append(response.html.search()[0]) #Scraping template
#    ' '.join(myString.split())
    title = ' '.join((response.html.search('<span id="productTitle" class="a-size-large">{}</span>'))).split()
    #title = " ".join(title)
    item_array.append(title) #extract the title
#  Extracting the price from 2 known design layouts
    if response.html.search('a-color-price inlineBlock-display offer-price a-text-normal price3P"><span class="currencyINR">&nbsp;&nbsp;</span>{}<') != None:
        item_array.append(response.html.search('a-color-price inlineBlock-display offer-price a-text-normal price3P"><span class="currencyINR">&nbsp;&nbsp;</span>{}<')[0]) #Extracting the current price
    elif response.html.search('a-color-price a-text-bold"><span class="currencyINR">&nbsp;&nbsp;</span> {}</span>') != None:
        item_array.append(response.html.search('a-color-price a-text-bold"><span class="currencyINR">&nbsp;&nbsp;</span> {}</span>')[0])
    else:
        item_array.append('0')      #0 - Not found
#Extracting the MRPs from the 2 known design layouts
    if response.html.search('<span class="a-color-secondary a-text-strike"><span class="currencyINR">&nbsp;&nbsp;</span> {}</span>') != None:
        item_array.append(response.html.search('<span class="a-color-secondary a-text-strike"><span class="currencyINR">&nbsp;&nbsp;</span> {}</span>')[0]) #Exracting the listed MRP
    else:
        item_array.append('0')
    print(item_array)



    #print(response.html.search('a-color-price inlineBlock-display offer-price a-text-normal price3P"><span class="currencyINR">&nbsp;&nbsp;</span>{}<')[0])
    #Extracting the text containing the product details
#print(all_items)
#Convert mmaster array to csv
#with open("new_file.csv","w+", encoding="utf-8") as my_csv:
#    csvWriter = csv.writer(my_csv,delimiter=',')
#    csvWriter.writerows(all_items)
