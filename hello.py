from flask import Flask, request, render_template
import pdb

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
    print ('dsfsdfsdf')
    print (text)
    print ('dsfsdfsdf')
    processed_text = text.upper()
    return render_template('result.html', result=processed_text)


@app.route('/', methods=['GET'])
def index():
    print ('i am called')
    return render_template('index.html')
