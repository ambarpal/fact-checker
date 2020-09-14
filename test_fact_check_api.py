# import requests
# import pdb

# api_url = 'https://factchecktools.googleapis.com/v1alpha1/claims:search'
# query = {'query': 'coronavirus is a type of rabies', 'key': 'AIzaSyCtfHm7PXk1ZD_vcXihKzUk5rNO287S0DY'}
# response = requests.get(api_url, params=query, headers={'Content-Type':'application/json'})
# if response.status_code != 200:
#     # This means something went wrong.
#     print ('DID NOT WORK!')
# else:
#     resp_json = response.json()
#     for claim in resp_json['claims']:
#         for review in claim['claimReview']:
#             print (review['textualRating'])
#         # print('{} {}'.format(todo_item['id'], todo_item['summary']))

# '''
# GET https://factchecktools.googleapis.com/v1alpha1/claims:search?query=is%20google%20real&key=AIzaSyCtfHm7PXk1ZD_vcXihKzUk5rNO287S0DY HTTP/1.1

# Accept: application/json


# curl \
#   'https://factchecktools.googleapis.com/v1alpha1/claims:search?query=is%20google%20real&key=955767f0032cf20f122a012549e42d11eb4f398c' \
#   --header 'Accept: application/json' \
#   --compressed

# {'text': 'Novel coronavirus is a virus, not a bacterium easily treated with aspirin', 
# 'claimant': 'Facebook',
# 'claimDate': '2020-05-28T00:00:00Z',
# 'claimReview': 
# [{'publisher': {'name': 'USA Today', 'site': 'usatoday.com'}, 'url': 'https://www.usatoday.com/story/news/factcheck/2020/05/29/fact-check-covid-19-caused-virus-not-bacteria/5277398002/', 'title': 'Fact check: COVID-19 is caused by a virus, not by bacteria', 'reviewDate': '2020-05-29T00:00:00Z', 'textualRating': 'False', 'languageCode': 'en'}]}
# '''

import requests
import pdb
import argparse
import re
from nltk.tokenize import RegexpTokenizer
from utils import get_true_false

api_url = 'https://factchecktools.googleapis.com/v1alpha1/claims:search'

def sanitizer1(sentence):
    sentence = sentence.strip().replace('-19', '')
    tokenizer = RegexpTokenizer('\w+|\$[\d\.]+||\-+')
    tokens = tokenizer.tokenize(sentence)
    sentence = " ".join([token.lower().strip() for token in tokens])
    sentence = re.sub(r'[ ]+',' ', sentence)
    sentence = sentence.replace('covid', 'corona virus').\
                        replace('coronavirus', 'corona virus').\
                        replace('sars-cov-2', 'corona virus').\
                        replace('  ', ' ')
    return sentence

def get_verdicts(question, verbose=True):
    query = {'query': question, 'key': 'AIzaSyCtfHm7PXk1ZD_vcXihKzUk5rNO287S0DY'}
    response = requests.get(api_url, params=query, headers={'Content-Type':'application/json'})
    if response.status_code != 200:
        # This means something went wrong.
        print ('DID NOT WORK!')
    else:
        resp_json = response.json()
        fact, verdict = [], []
        for claim in resp_json['claims']:
            sentence = sanitizer1(claim['text'])
            fact.append(sentence)
            #print(sentence)
            for review in claim['claimReview']:
                #print ('\t' + review['textualRating'])
                verdict.append(review['textualRating'])
        res_scores = get_true_false(verdict)
        res = []
        for i in range(len(fact)):
            cur_res = (fact[i], res_scores[i], verdict[i])
            res.append(cur_res)
            if verbose:
                print(cur_res[0],'\n',cur_res[1],'original verdict: ',cur_res[2])
        return res

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("q", help="enter query", type=str)
    args = parser.parse_args()

    res_verdicts = get_verdicts(args.q, verbose=True)
    for v in res_verdicts:
        print (v[1])



## API: https://developers.google.com/fact-check/tools/api/reference/rest/v1alpha1/claims#Claim


















