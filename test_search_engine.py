import requests
import pdb
import argparse
from nltk.tokenize import RegexpTokenizer
import re
from utils import get_scores, sanitizer2

# api_url = 'https://www.googleapis.com/customsearch/v1?&cx=0156ca17ee72cb816&q=is%20covid%20a%20virus'
api_url = 'https://www.googleapis.com/customsearch/v1'
threshold_high = 0.8
threshold_low = 0.8

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
        if top_score >= threshold_high:
            res = 1
            if verbose: print ("TRUE")
        elif top_score < threshold_low:
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
    ("i should not wear masks while exercising", True), 
    ("there a cure for the coronavirus", False),
    ("the pneumonia vaccine will immunise me against the coronavirus", False),
    ("Mosquito bites spread the coronavirus", False),
    ("The coronavirus spreads in hot or cold climates", True),
    ("I can recover from the coronavirus", True),
    ("Children do not spread the corona virus", False),
    ("Drinking cow urine prevents corona virus", False)
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("q", help="enter query", type=str)
    args = parser.parse_args()
    res = check_true(sanitizer2(args.q), verbose=True)
    print ('RESULT:', res)
    
    '''
    print ('Calculating Accuracy on Entire Data...')
    acc = 0.0
    tot_num = 0
    for question, answer in data:
        pred = check_true(question, verbose=True)
        tot_num += 1.0

        if pred != answer: 
            print (question, "Incorrect")
        else:
            acc += 1.0
            print (question, "Correct")

    acc /= tot_num
    print ("Accuracy: ", acc * 100.0)
    '''





