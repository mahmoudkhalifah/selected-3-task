# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 22:22:42 2021

@author: Mahmoud
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


df = pd.read_csv('Books.csv')
df = df.dropna(axis=0)
#print(df.info())

X = df['summary']
print(X.head())
print(X[0])


y = df['Section']
print(y.tail())
print(y[0])

count = CountVectorizer()
count.fit(X)
X=count.transform(X)
#print(X.toarray())


l = LabelEncoder()
y = l.fit_transform(y)
classes = l.classes_

#print(l.classes_)
print(y)


x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.2)


clf= MultinomialNB().fit(x_train, y_train)

print(clf.score(x_test, y_test))



