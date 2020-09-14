import requests
import pdb
import argparse
from nltk.tokenize import RegexpTokenizer
import re
from utils import get_scores, sanitizer2

# api_url = 'https://www.googleapis.com/customsearch/v1?&cx=0156ca17ee72cb816&q=is%20covid%20a%20virus'
api_url = 'https://www.googleapis.com/customsearch/v1'
threshold_high = 0.78
threshold_low = 0.78

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

data_covid_fact_check = [
    ('Continue to stay 6 feet away from each other', True),
    ('Wash hands before and after putting on a mask', True),
    ('Mask that fits prevents spreading of respiratory droplets while speaking, coughing or sneezing', True),
    ('The virus lives on cardboard for up to 24 hours, steel and plastic up to 72 hours', True),
    ('Cleaned touched surfaces at home frequently', True),
    ('Ibuprofen does not worsen COVID-19 symptoms', True),
    ('Please do not self-medicate', True),
    ('Hydroxychloroquine, chloroquine, and azithromycin does not prevent COVID-19', True),
    ('People of all ages can contract the virus', True),
    ('Older and immunocompromised individuals are more vulnerable to becoming severely ill', True),
    ('Holding your breath for 10 secs or longer is not a test for COVID-19', True),
    ('Breathing exercises are not a test for COVID-19', True),
    ('Hand dryers do not kill the coronavirus', True),
    ('UV light should not be used to sterilize your hands', True),
    ('Wash your hands with soap and water or alcohol-based hand rub', True),
    ('Rinsing your nose with saline does not prevent COVID-19', True),
    ('Extremely hot showers or baths do not prevent COVID-19', True),
    ('Cold weather and snow cannot prevent COVID-19', True),
    ('Eating garlic does not protect you from the coronavirus', True),
    ('Drinking alcohol does not protect you against COVID-19', True),
    ('Excessive alcohol can be dangerous and increase health problem risk', True)
]

data_cdc = [
    ('Bluelips or face is one the symptoms of COVID', True),
    ('Asymptomatic people do not spread COVID', True),
    ('You should stay in quarantine for 14 days after close contact with the person who has COVID-19', True),
    ('Do not travel if you have COVID', True),
    ('N95 mask offers more protection than surgical mask', True),
    ('Is it necessary to wear PPE', True),
    ('Coronavirus spreads from people to animals', True),
    ('Pets test positive for COVID', True),
    ('Pets have died from coronavirus infection', True),
    ('Pets need to be isolated if tested positive for coronavirus', True),
    ('You can go hiking in this pandemic', True),
    ('COVID-19 infected people lose sense of taste and smell', True),
    ('Coronavirus does not affect periods/menstrual cycle', True),
]

data_nasem = [
    ('Applying heat to your skin or throat does not kill the coronavirus', True), 
    ('There are no food, drinks, or supplements that will protect you from COVID-19', True), 
    ('COVID-19  is not like the flu', True), 
    ('The virus lives on printing paper and tissue paper for 3 hours', True), 
    ('The virus lives on copper for 4 hours, cloth for 2 day, wood for 2 days, paper money for 4 days, and glass for 4 days', True), 
    ('The virus lives on plastic for 3 to 7 days', True), 
    ('The stainless steel lives on plastic for 2 to 7 days', True), 
    ('A small amount of viable plastics stay on surgical masks after 7 days', True), 
    ('Washing your hands with soap and water for 20 secs is effective in protecting against the coronavirus', True), 
    ('Copper supplement will not prevent, fight or cure a COVID infection', True), 
    ('Lemon juice will not prevent or cure a COVID-19 infection, no matter what is mixed with it', True), 
    ('The flu vaccine does not cause you to test positive for the COVID-19 test', True), 
    ('The flu vaccine does not interfere with your ability to fight the coronavirus', True), 
    ('Consuming ginger will not prevent or cure COVID-19', True), 
    # ('There is no evidence that witch hazel destroys germs, including the novel coronavirus', True), 
    ('You should wear sunblock', True)
]

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument("q", help="enter query", type=str)
    # args = parser.parse_args()
    # res = check_true(sanitizer2(args.q), verbose=True)
    # print ('RESULT:', res)

    print ('Calculating Accuracy on Entire Data...')
    acc = 0.0
    tot_num = 0
    for question, answer in data_nasem:
        pred = check_true(question, verbose=False)
        tot_num += 1.0

        if pred != answer: 
            print (question, "Incorrect")
        else:
            acc += 1.0
            print (question, "Correct")

    acc /= tot_num
    print ("Accuracy: ", acc * 100.0)





