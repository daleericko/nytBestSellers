# Webscrape NYT best selling books 

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pyprojroot import here
from datetime import datetime

# Setup file path for final csv output
path_to_output = here('data-output')
todaysDate = datetime.today().strftime('%Y-%m-%d')

# GET request
url = "https://www.nytimes.com/books/best-sellers/hardcover-nonfiction/"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

# define a function to get the "soup"
def getNytText(tag, myClass):
  myList = soup.find_all(str(tag), class_=str(myClass))
  return(myList)

# Create a dataframe that contains the items we need to iterate through
nytDf = pd.DataFrame({
  'infoItem': [
    'weeksOnList', 
    'title', 
    'author', 
    'publisher', 
    'abstract'
  ], 
  'tag': [
    'p', 
    'h3', 
    'p', 
    'p', 
    'p'
  ], 
  'class': [
    'css-1o26r9v', 
    'css-5pe77f', 
    'css-hjukut', 
    'css-heg334', 
    'css-14lubdp'
  ]
})

def makeNytDf(infoItem, tag, class_name):
  # get the "soup"
  infoItem = getNytText(str(tag), str(class_name))

  # create our empty list
  output = []

  # iterate  through all objects in our "soup"
  for item in infoItem:
    output.append(item.get_text().title()) # make title case too

  return(output)

scrapedNyt = pd.DataFrame(map(makeNytDf, nytDf['infoItem'], nytDf['tag'], nytDf['class'])).transpose().rename(columns = nytDf['infoItem'])

# remove the word "by" from the author series
scrapedNyt['author'] = scrapedNyt['author'].map(lambda x: x.lstrip('By '))

print(scrapedNyt)

# Save to output folder 
scrapedNyt.to_csv(str(path_to_output) + '/' + str(todaysDate) + '_nytBestSellers.csv', index = False)

print('Please find your file in the data-output folder')
###