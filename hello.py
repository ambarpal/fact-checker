from flask import Flask, request, render_template
import pdb
import torch
import sys


import os
print(os.getcwd())

#ishita's laptop does not support bert
if os.getcwd() != 'C:\\Users\\sakur\\Desktop\\Hophacks\\website\\fact-checker':
    from test_search_engine import check_true

app = Flask(__name__)


# @app.route('/')
# def index():
#     posts = [{'title': 'Some Title', 'created': '21 jan'}]
#     return render_template('index.html', posts=posts)


'''
@app.route('/<string:query>')
def post(query):
    res = query + " Hello"
    # pdb.set_trace()
    return render_template('result.html', result=res)
'''

@app.route('/', methods=['POST'])
def post2():
    print('here')
    text = request.form['query']
    response = check_true(text)
    response = text.upper()
    return render_template('result.html', result=response)


@app.route('/', methods=['GET'])
def index():
    print ('i am called')
    return render_template('index.html')
