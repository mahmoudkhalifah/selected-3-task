# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 20:18:22 2021

@author: moham
"""
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r"\w+")
from Model import Search_class
from flask import Flask , render_template,url_for,request
app = Flask(__name__)


def clear_query(query):
    query = tokenizer.tokenize(query)
    query =' '.join(query) 
    return(query)

@app.route('/')
def Main():
    return render_template("Main.html")

@app.route('/Search',methods=['POST'])
def Search():
    data = request.form
    query = data['search_query']
    model = Search_class()
    
    if query:
        query = clear_query(query)
        t = model.search(query)
        return render_template("Main.html",Dict = t)
    else:
        return render_template("Main.html")

if __name__ == '__main__':
   app.run(debug = True)
   

##app.route(rule, options)
#app.run(host, port, debug, options)

#EXPORT FLASK_APP=HomePage.py
# flask run



