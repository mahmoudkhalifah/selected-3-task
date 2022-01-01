# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import bs4 as BeautifulSoup
import requests
import itertools   
import re 
from nltk.tokenize import TweetTokenizer
tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,reduce_len=True) 
from textblob_ar import TextBlob
from textblob_ar.correction import TextCorrection


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

stop_words = ["PDF","pdf","كتاب","رواية","مجلة"]

for book in Books:
    if book[0]:
        Name = tokenizer.tokenize(book[0])
        New_Name = []
        for n in Name:
            if n not in stop_words: 
               # if not n.isdigit():
                    #n = TextCorrection().correction(n, top=True)
                New_Name.append(n)
            
        New_Name =' '.join(New_Name) 
        book[0] = New_Name
        print(New_Name)

BookNames = []
Authors = []
download_links = []
for book in Books:
    BookNames.append(book[0])
    #Authors.append(book[1])
    #download_links.append(book[2])

#Remove stop words and white spaces from authors names
stop_words = ["الكاتب","الدكتور","الناشر","الباحث","المؤلف","أستاذ","دكتور"]
NewAuthors = []
for auth in Authors:
    B_Name = []
    tokens = tokenizer.tokenize(auth)
    for token in tokens:
        if token not in stop_words:
            B_Name.append(token)
    B_Name = ' '.join(B_Name)
    NewAuthors.append(B_Name)
Authors = NewAuthors




#response = requests.get(download_links[3575])
#soup = BeautifulSoup.BeautifulSoup(response.content, 'html.parser')  
#ReadLinks.insert(3314,"")


qesm = []
Countofpages = []
darNashr = []
BookSize = [] 
Molakhas = []
ReadLinks = []
count = 3576
for url in download_links[count:]:
    if not count == 3314 or not count == 3575:
        response = requests.get(url)
        soup = BeautifulSoup.BeautifulSoup(response.content, 'html.parser')  
        
        bookDetails = soup.find("div",class_='book-info')
        #print(bookDetails)
        allLi = bookDetails.findAll("li")
        #print(allLi[5].text)
        qesm.append(allLi[1].text)
        Countofpages.append(allLi[3].text)
        darNashr.append(allLi[4].text)
        BookSize.append(allLi[5].text)
        
        wasf = soup.find("div",class_='entry-content entry clearfix')
        wasf = wasf.findAll("p")
        wasf = wasf[0:4]
        Molakhas.append(wasf)
        
        ReadLink = soup.find("div",class_='read-link-bottom')
        ReadLinks.append(ReadLink)
    else :
        qesm.append("")
        Countofpages.append("")
        darNashr.append("")
        BookSize.append("")
        Molakhas.append("")
        ReadLinks.append("")

    print(count)
    count+=1


stop_words = ["تحميل","قسم",":","الكتاب:","الكتاب"]
Section = []

for q in qesm:
    if q:
        tokens = tokenizer.tokenize(q)
        New_q = []
        for token in tokens:
            if token not in stop_words: 
                New_q.append(token)
            
        New_q =' '.join(New_q) 
    Section.append(New_q)
    print(New_q)
    
    
stop_words = ["الص","صفحة",":","عدد","فحات",'ّ']
Nofpages = []

for c in Countofpages:
    if c:
        tokens = tokenizer.tokenize(c)
        New_c = 0
        for token in tokens:
            if token not in stop_words: 
                New_c = token
            
        #New_c =' '.join(New_c) 
    Nofpages.append(New_c)
    print(New_c)
    
    
stop_words = ["النشر:",":النشر",":","النشر","-"]
publishing_house = []

for p in darNashr:
    if p:
        tokens = tokenizer.tokenize(p)
        if tokens[0] == "دار":
            del tokens[0]
        New_p = []
        for token in tokens:
            if token not in stop_words: 
                New_p.append(token)
            
        New_p =' '.join(New_p) 
    publishing_house.append(New_p)
    print(New_p)
    
stop_words = ["حجم",":","الكتاب:","الكتاب"]
Size = []

for s in BookSize:
    if s:
        tokens = tokenizer.tokenize(s)
        New_s = []
        for token in tokens:
            if token not in stop_words: 
                New_s.append(token)
            
        New_s =' '.join(New_s) 
    Size.append(New_s)
    print(New_s)
    

summary = []
for m in Molakhas:
    print(Molakhas.index(m))
    if len(m) == 1:
        if m:
            summary.append(m)
    elif len(m) == 0:
        summary.append("")
    else:
        new_m = ""
        for index in range(2):
            new_m+=m[index].text
            new_m+=" "
        summary.append(new_m)
        
stop_words = pd.read_csv('H:/4/Selected 3/Project/Stop_words.txt')
stop_words = stop_words.values.tolist()
tags = ["<p>","</p>","<a>","</a>","pdf","PDF","span","<","</span>","<br/>","class","morecontent","="]
Summary = []
for s in summary:
    new_s = []
    tokens = tokenizer.tokenize(str(s))
    for token in tokens:
        if not token in stop_words and not token in tags:
            new_s.append(token)
    new_s =' '.join(new_s)
    Summary.append(new_s)
summary = Summary
    
ReadingLinks = []
for r in ReadLinks:  
    tokens = tokenizer.tokenize(str(r))
    islink = False
    for token in tokens:
        if re.findall(r'^https?:\/\/.*[\r\n]*', token):
           ReadingLinks.append(token)  
           islink = True
    if not islink:
        ReadingLinks.append("")




df = pd.DataFrame({"title":BookNames,"Author":Authors,"Section":Section,"Nofpages":Nofpages,"publishing_house":publishing_house,"Size":Size,"summary":summary,"linkforpdf":ReadingLinks})
df.to_csv('H:/4/Selected 3/Project/Books.csv',index = False,encoding='utf-8-sig')




