import requests
import pdb
import argparse
from nltk.tokenize import RegexpTokenizer
import re
from test_bert import get_scores

parser = argparse.ArgumentParser()
parser.add_argument("q", help="enter query", type=str)
args = parser.parse_args()

api_url = 'https://www.googleapis.com/customsearch/v1?&cx=0156ca17ee72cb816&q=is%20covid%20a%20virus'
query = {
    'key': 'AIzaSyCtfHm7PXk1ZD_vcXihKzUk5rNO287S0DY', 
    'cx': '0156ca17ee72cb816', 
    'q': args.q
}
response = requests.get(api_url, params=query, headers={'Content-Type':'application/json'})
if response.status_code != 200:
    # This means something went wrong.
    print ('DID NOT WORK!')
else:
    resp_json = response.json()
    snippets = []
    for item in resp_json['items']:
        snippet = item['snippet'].replace('...', '.').replace('-19','').replace(' 19', '')
        tokenizer = RegexpTokenizer('\w+|\$[\d\.]+||\-+')
        tokens = tokenizer.tokenize(snippet)
        sentence = " ".join([token.lower().strip() for token in tokens])
        # if the 2 and 3rd tokens are numbers, replace the first 3 tokens
        sentence = re.sub(r'[ ]+',' ', sentence)
        sentence = re.sub(r'^[a-z]+[ ]+[0-9]{1,2}[ ]+[0-9]{4}[ ]+', '',sentence)
        sentence = sentence.replace('covid', 'corona virus').replace('coronavirus', 'corona virus').replace('sars-cov-2', 'corona virus').\
                    replace('  ', ' ')
        snippets.append(sentence)
        #print ('\'' + item['snippet'].rstrip('...').lstrip('...') + '\'')
        # print (item['formattedUrl'])
        # print ('#############')
    print('\n'.join(snippets))

    get_scores(snippets, args.q)

    