import requests
import pdb
import argparse
from nltk.tokenize import RegexpTokenizer
import re
from test_bert import get_scores, sanitizer2

# api_url = 'https://www.googleapis.com/customsearch/v1?&cx=0156ca17ee72cb816&q=is%20covid%20a%20virus'
api_url = 'https://www.googleapis.com/customsearch/v1'

def check_true(question, verbose=True):
    query = {
        'key': 'AIzaSyCtfHm7PXk1ZD_vcXihKzUk5rNO287S0DY', 
        'cx': '0156ca17ee72cb816', 
        'q': question
    }
    response = requests.get(api_url, params=query, headers={'Content-Type':'application/json'})
    if response.status_code != 200:
        # This means something went wrong.
        print ('DID NOT WORK!')
    else:
        # pdb.set_trace()
        resp_json = response.json()
        snippets = []
        for item in resp_json['items']:
            sentence = sanitizer2(item['snippet'])
            # snippet = item['snippet'].replace('...', '.').replace('-19','').replace(' 19', '')
            # tokenizer = RegexpTokenizer('\w+|\$[\d\.]+||\-+')
            # tokens = tokenizer.tokenize(snippet)
            # sentence = " ".join([token.lower().strip() for token in tokens])
            # # if the 2 and 3rd tokens are numbers, replace the first 3 tokens
            # sentence = re.sub(r'[ ]+',' ', sentence)
            # sentence = re.sub(r'^[a-z]+[ ]+[0-9]{1,2}[ ]+[0-9]{4}[ ]+', '',sentence)
            # sentence = sentence.replace('covid', 'corona virus').replace('coronavirus', 'corona virus').replace('sars-cov-2', 'corona virus').\
            #             replace('  ', ' ')
            snippets.append(sentence)
            #print ('\'' + item['snippet'].rstrip('...').lstrip('...') + '\'')
            # print (item['formattedUrl'])
            # print ('#############')
        if verbose:
            print('\n'.join(snippets))

        res_scores = get_scores(snippets, question, verbose=verbose)
        
        if verbose:
            print ('RES SCORES')
            print (res_scores)

        top_score = res_scores[0][1]
        if top_score >= 0.7:
            res = 1
            if verbose: print ("TRUE")
        elif top_score <= 0.5:
            res = 0
            if verbose: print ("FALSE")
        else:
            res = 0.5
            if verbose: print ("WE ARE UNSURE")
        return res

    return res

data = [
    ("corona virus is not a hoax", True), 
    ("corona virus is a hoax", False), 
    ("corona virus is not a conspiracy theory", True),
    ("corona virus is a conspiracy theory", False),
    ("corona virus was made in a lab", False), 
    ("corona virus was man made", False),
    ("corona virus is a bio weapon", False), 
    ("corona virus causes cancer", False), 
    ("corona virus causes hiv", False), 
    ("injecting bleach kills does not kill corona virus", True), 
    ("there is a hidden cure for corona virus", False), 
    ("corona virus is the deadliest virus", False),
    ("corona virus emerged in wuhan", True), 
    ("corona virus originated in wuhan", True),
    ("corona virus is a virus", True), 
    ("there is no vaccine for coronavirus", True), 
    ("pneumonia vaccine would protect me from corona virus", False), 
    ("drinking sanitizers prevents corona virus", False),
    ("i should not wear masks while exercising", True)
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("q", help="enter query", type=str)
    args = parser.parse_args()
    res = check_true(args.q, verbose=False)
    print (res)

    # acc = 0.0
    # tot_num = 0
    # for question, answer in data:
    #     pred = check_true(question, verbose=False)
    #     tot_num += 1.0

    #     if pred != answer: 
    #         print (question, "Incorrect")
    #     else:
    #         acc += 1.0
    #         print (question, "Correct")

    # acc /= tot_num
    # print ("Accuracy: ", acc)






