# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import bs4 as BeautifulSoup

import requests
import itertools


import string    
import re 


url = "https://www.arab-books.com/"    
response = requests.get(url)
soup = BeautifulSoup.BeautifulSoup(response.content, 'html.parser')  
BookNames = []
Authors = []
download_links = []


for book in soup.findAll("li",class_='post-item tie-standard'):
    name = book.find('h3')
    author = soup.find("div",class_='book-writer') 
    Link = soup.find("div",class_ = 'book-download')
    BookNames.append(name.text)
    Authors.append(author.text)
    download_links.append(Link)
    


url = "https://www.arab-books.com//page/{}"
for page in itertools.count(start=2):
    response = requests.get(url.format(page))
    soup = BeautifulSoup.BeautifulSoup(response.content, 'html.parser') 
    author = soup.findAll("div",class_='book-writer')
    Link = soup.findAll("div",class_ = 'book-download')
    x = 0
    for book in soup.findAll("li",class_='post-item tie-standard'):
       name = book.find('h3')
       BookNames.append(name.text)
       Authors.append(author[x].text)
       download_links.append(Link[x])
       x += 1
       
    print(page)
    if not soup.findAll("li",class_='post-item tie-standard'):
        break


Books = []
for x in range(len(BookNames)):
    Books.append([BookNames[x],Authors[x],download_links[x]])
    
    

from nltk.tokenize import TweetTokenizer
tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,reduce_len=True) 


#Remove duplications
for book in Books:
    b = tokenizer.tokenize(book[1])
    if len(b) % 2 == 0 and len(b) > 0:
    #print(b)
        if b[0] == b[len(b)//2]:
            b = b[:len(b)//2]
        b=' '.join(b)  
        book[1] = b
                               
#get link from tag
for book in Books:
    link = tokenizer.tokenize(str(book[2]))
    for token in link:
        if re.findall(r'^https?:\/\/.*[\r\n]*', token):
            book[2] = token
            



from textblob_ar import TextBlob
from textblob_ar.correction import TextCorrection
import os


stop_words = ["PDF","pdf"]

for book in Books:
    if book[0]:
        Name = tokenizer.tokenize(book[0])
        New_Name = []
        for n in Name:
            if n not in stop_words: 
                if not n.isdigit():
                    n = TextCorrection().correction(n, top=True)
                New_Name.append(n)
            
        New_Name =' '.join(New_Name) 
        book[0] = New_Name
        print(New_Name)





BookNames = []
Authors = []
download_links = []
for book in Books:
    BookNames.append(book[0])
    Authors.append(book[1])
    download_links.append(book[2])
# Author - title - publishing year - link for pdf - etc.
df = pd.DataFrame({"Author":BookNames,"title":Authors,"linkforpdf":download_links})
df.to_csv('H:/4/Selected 3/Bookss.csv',index = False,encoding='utf-8-sig')

print(BookNames)

print(df.Author)























