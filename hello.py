from flask import Flask, request, render_template
import pdb
import torch
import sys
import os

#ishita's laptop does not support BERT
if os.getcwd() != 'C:\\Users\\sakur\\Desktop\\Hophacks\\website\\fact-checker':
    print(os.getcwd())
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
    try:
        #response = check_true(text)
        response = 0
        response = ['False', 'Unsure', 'True'][response * 2]
    except:
        response = 'Unsure'

    return render_template('results2.html', result=response)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')


'''
<!--
{{@for_{variable in variable}}
<div class='source'> {{ variable['text'] }} </div>
{{end_for}}}
-->
'''
