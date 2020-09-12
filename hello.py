from flask import Flask, request, render_template
import pdb
import torch
import sys
import os

#ishita's laptop does not support BERT
if os.getcwd() != 'C:\\Users\\sakur\\Desktop\\Hophacks\\website\\fact-checker':
    sys.path.insert(0, './cis/home/ambar/my_documents/docker-data/com/hophacks20')
    from test_search_engine import check_true

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# @app.route('/<string:query>')
# def post(query):
#     res = query + " Hello"
#     # pdb.set_trace()
#     return render_template('result.html', result=res)

@app.route('/', methods=['POST'])
def post2():
    print('here')
    text = request.form['query']
    response = check_true(text)
    return render_template('result.html', result=response)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    



