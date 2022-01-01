# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 22:31:23 2021

@author: Mahmoud

import nltk
nltk.download('stopwords')
"""
import pandas as pd
import nltk

stop_words = set(nltk.corpus.stopwords.words("arabic"))
'''pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)'''

df = pd.read_csv('Books.csv')

X = df['summary']

#print(X)

X = X.dropna(axis=0)

from sklearn.feature_extraction.text import TfidfVectorizer
cv_tfidf = TfidfVectorizer(stop_words=stop_words)
X_tfidf = cv_tfidf.fit_transform(X).toarray()
tfidf = pd.DataFrame(X_tfidf,columns=cv_tfidf.get_feature_names())
#print(dt_tfidf.columns.values.tolist())

#from textblob import TextBlob

keywords = []

for col in tfidf.columns:
    #print(tfidf[col].max())
 #   word = TextBlob(col)
    if tfidf[col].max() > 0.5:
        if not col.isdigit():
            keywords.append(col)

print(keywords)
print(len(keywords))
print(len(tfidf.columns))

