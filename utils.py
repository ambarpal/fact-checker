import spacy
from spacy import displacy

from sentence_transformers import SentenceTransformer, util
import numpy as np
import pdb
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
import re
import torch

embedder = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

# Corpus with example sentences
# corpus = ['A man is eating food.',
#           'A man is eating a piece of bread.',
#           'The girl is carrying a baby.',
#           'A man is riding a horse.',
#           'A woman is playing violin.',
#           'Two men pushed carts through the woods.',
#           'A man is riding a white horse on an enclosed ground.',
#           'A monkey is playing drums.',
#           'A cheetah is running behind its prey.'
#           ]

# corpus = [
# 'Corona virus disease corona virus is an infectious disease caused by a newly discovered corona virus. Most people infected with the corona virus will',
# 'Information on corona virus the infectious disease caused by the most recently discovered corona virus',
# 'FACT: The corona virus disease corona virus is caused by a virus, NOT by bacteria. The virus that causes corona virus in a family of viruses called Coronaviridae', 
# 'An explanation of the official names for the corona virus disease corona virus and the virus that causes it', 
# 'According to current evidence,corona virus is primarily transmitted between people through respiratory droplets and contact routes.2-7 In an ',
# 'How is the virus that causes corona virus most commonly transmitted between people? Current evidence suggests that corona virus spreads ',
# 'Current evidence suggests that SARS-CoV-2, the virus that causes corona virus is predominantly spread from person-to-person. Understanding ',
# 'How are corona virus and influenza viruses similar? The serial interval for corona virus is estimated to be 5-6 days, while for influenza virus, ',
# 'Current understanding of transmission risk. Infection with the virus causing corona virus SARS-CoV-2) is confirmed by the presence of viral RNA ',
# 'Droplets spread virus. By following good respiratory hygiene, you protect the people around you from viruses such as cold, flu andcorona virus', 
# 'corona virus is a hoax', 
# 'tarana wants to sleep']
# queries ['coronavirus is a virus']

# corpus = [
# 'FACT: Vaccines against pneumonia doesn\'t protect against the corona virus',
# 'FACT: Vaccines against pneumonia protects against the corona virus',
# 'WHO continues to recommend neonatal BCG vaccination in countries or WHO does not recommend BCG vaccination for the prevention of corona. BCG Vaccination to Protect Healthcare Workers Against corona ',
# 'Fact sheet from WHO on immunization coverage: provides key facts and information (DTP3) vaccine, protecting them against infectious diseases that can cause. Haemophilus influenzae type b (Hib) causes meningitis and pneumonia. the use of vaccines to protect people of all ages against disease',
# 'As the world waits for a vaccine to defeat the corona pandemic, we. This level of protection comes through a strong global effort to increase vaccine and pneumonia, diarrhoea, and the worlds first-ever malaria vaccine so that when we have a safe and effective vaccine, no one will be left behind',
# 'Many vaccines can also protect when administered after exposure – examples. In field trials, mortality and morbidity reductions were seen for pneumococcal ',
# 'Vaccines reduce risks of getting a disease by working with your body natural defences to build protection. When you get a vaccine, your immune system ',
# 'disease corona and on next steps in readiness and with pneumonia of unknown etiology – a surveillance definition established following the. However, they do not appear to be major drivers of the overall measures to slow transmission of the corona virus, reduce disease and save lives',
# 'Most people infected with the corona virus will experience mild to moderate. Protect yourself and others from infection by washing your hands or using an alcohol At this time, there are no specific vaccines or treatments for corona', 
# 'Despite their success in preventing disease, vaccines rarely protect 100 of the recipients. Administration of other vaccines will be advised on the basis of a travel risk. Important cause of pneumonia, meningitis, septicaemia, epiglottitis and',
# 'Myth 2: The flu vaccine can give me the flu. Fact: The However, being vaccinated improves the chance of being protected from the flu. This is especially'
# ]
# queries = ['there is no vaccine for coronavirus']

# corpus = [
# 'Rabies is a zoonotic disease (a disease that is transmitted from animals to humans, Furious rabies is the most common form of human rabies, accounting for ',
# 'Rabies infection manifests in two forms of rabies: furious (classical or encephalitic) form and the paralytic form. Furious rabies accounts for approximately 80 of',
# 'Paralytic rabies accounts for about 20 of the total number of human cases. This form of rabies runs a less dramatic and usually longer course',
# 'Rabies is a viral zoonotic disease that causes progressive and fatal inflammation of the brain and spinal cord',
# 'Rabies is estimated to cause 59 000 human deaths annually in over 150 countries, with 95 of cases occurring in Africa and Asia. Due to widespread ',
# 'Children are at particular risk. Two types of vaccines to protect against rabies in humans exist - nerve tissue and cell culture vaccines. WHO recommends ',
# 'Recommendations for post-exposure depend on the type of contact with the suspected rabid animal. For category I exposure (touching or ',
# 'Rabies is a significant health concern following dog bites, cat bites and The health impacts of animal bites are dependent on the type and ',
# 'Human rabies is a 100% vaccine-preventable disease, yet it continues to kill. Rabies vaccinations are highly effective, safe and well tolerated. The WHO ',
# 'Over the past few years, many countries have acted to strengthen rabies control efforts—scaling up dog vaccination programmes, making human'
# ]
# queries = ['would pneumonia vaccine protect me from corona virus']

corpus = [
'Highlighting some of the misinformation circulating on COVID-19. Bleach and disinfectant should be used carefully to disinfect surfaces only. Drinking methanol, ethanol or bleach DOES NOT prevent or cure COVID-19 and can be ', 
'Keep alcohol-based hand sanitizers out of childrens reach. Apply a coin-sized amount on your hands. Avoid touching your eyes, mouth and '
'Regularly wash hands with soap and water or alcohol-based hand sanitizer Fact: There is no scientific evidence that lemon/turmeric prevents COVID-19',
'Todays handrubs all contain skin softeners which help prevent drying. Of the published studies available, many describe that nurses who routinely use alcohol',
'for preventing and for protecting human health during all infectious disease outbreaks, including of coronavirus disease 2019 (COVID-19)',
'Consequently, hand hygiene is extremely important to prevent the spread of the COVID-19 virus. It also interrupts transmission of other viruses and bacteria ',
'Q&A: Considerations for the cleaning and disinfection of environmental surfaces in the context of COVID-19 in non-health care settings ',
'How can you clean soiled bedding, towels and linens from patients with COVID-19?',
'Simple ways to prevent the spread of COVID-19 in your workplace. 2. How to Put sanitizing hand rub dispensers in prominent places around the workplace. Encourage regular hand-washing or use of an alcohol rub by all ',
'Alternative drinking-water disinfectants: bromine, iodine and silver. used; these are generally used to prevent the silver nanoparticles from aggregating or '
]
question = 'drinking sanitizers prevents COVID-19'

# corpus = [
# 'People should NOT wear masks when exercising, as masks may reduce the ability The important preventive measure during exercise is to maintain physical',
# 'Should children with developmental disabilities wear masks? Should children wear a mask when playing sports or doing physical activities?',
# 'other equally relevant measures should be adopted. If masks are to be Wearing medical masks when not indicated may cause unnecessary',
# 'Why do we need it? Regular So how do I stay safe while exercising in COVID-19? Do not How do I stay active in and around the home?',
# 'Advice on the use of masks in the context of COVID-19. Interim guidance. Infection prevention and control / WASH. AddThis Sharing',
# 'Does WHO recommend routine wearing masks for healthy people during the 2019 nCoV outbreak?',
# 'Masks on their own will not protect you from COVID-19. person at home should wear a medical mask while they are in the same room as the ',
# 'Media Statement: the role and need of masks during COVID-19 outbreak. “If you do not wear the mask properly, touch the mask with unwashed hands, Before putting on a mask, clean hands with soap and running water or ',
# 'COVID-19 transmission & disease severity in young people. Guidance on 5 years and younger should not be required to wear masks. Questions about how to stay safe while exercising and how to stay active at ',
# 'But how do you do this in Senegal, where there are more than a dozen languages? In a bid to A woman exercises while wearing a face mask in Dakar, Sengal. ... In this new COVID era, however, it is not so much a time for concerts as it is for'
# ]
# queries = ['i should not wear masks while exercising']

who_truths = \
['Studies show hydroxychloroquine does not have clinical benefits in treating COVID-19',
'People should NOT wear masks while exercising',
'The likelihood of shoes spreading COVID-19 is very low',
'The coronavirus disease (COVID-19) is caused by a virus', 
'COVID-19 is NOT caused by bacteria',
'The prolonged use of medical masks* when properly worn DOES NOT cause CO2 intoxication nor oxygen deficiency',
'Most people who get COVID-19 recover from it',
'Drinking alcohol does not protect you against COVID-19 and can be dangerous',
'Thermal scanners CANNOT detect COVID-19',
'There are currently no drugs licensed for the treatment or prevention of COVID-19',
'Adding pepper to your soup or other meals DOES NOT prevent or cure COVID-19',
'COVID-19 is NOT transmitted through houseflies',
'Spraying and introducing bleach or another disinfectant into your body WILL NOT protect you against COVID-19;and can be dangerous',
'Drinking methanol ethanol or bleach DOES NOT prevent or cure COVID-19 and can be extremely dangerous',
'Drinking sanitizers DOES NOT prevent or cure COVID-19 and can be extremely dangerous',
'5G mobile networks DO NOT spread COVID-19',
'Exposing yourself to the sun or temperatures higher than 25&deg;C DOES NOT protect you from COVID-19',
'Catching COVID-19 DOES NOT mean you will have it for life',
'Being able to hold your breath for 10 seconds or more without coughing or feeling discomfort DOES NOT mean you are free from COVID-19',
'The COVID-19 virus can spread in hot and humid climates',
'Cold weather and snow CANNOT kill the COVID-19 virus',
'Taking a hot bath does not prevent COVID-19',
'Hand dryers are NOT effective in killing the COVID-19 virus',
'Ultra-violet (UV) lamps should NOT be used to disinfect hands or other areas of your skin',
'Vaccines against pneumonia DO NOT protect against the COVID-19 virus',
'Rinsing your nose with saline does NOT prevent COVID-19 ',
'Eating garlic does NOT prevent COVID-19',
'People of all ages can be infected by the COVID-19 virus',
'Antibiotics CANNOT prevent or treat COVID-19']

def sanitizer2(sentence):
    sentence = sentence.replace('...', '.').replace('-19','').replace(' 19', '')
    tokenizer = RegexpTokenizer('\w+|\$[\d\.]+||\-+')
    tokens = tokenizer.tokenize(sentence)
    sentence = " ".join([token.lower().strip() for token in tokens])
    # if the 2 and 3rd tokens are numbers, replace the first 3 tokens
    sentence = re.sub(r'[ ]+',' ', sentence)
    sentence = re.sub(r'^[a-z]+[ ]+[0-9]{1,2}[ ]+[0-9]{4}[ ]+', '',sentence)
    sentence = sentence.replace('covid', 'corona virus').replace('coronavirus', 'corona virus').replace('sars-cov-2', 'corona virus').\
                replace('  ', ' ')
    return sentence

def nltk_similarity(sa, sb):
    sa = sanitizer2(sa)
    sb = sanitizer2(sb)

    # tokenization 
    X_list = word_tokenize(sa)  
    Y_list = word_tokenize(sb) 
      
    # sw contains the list of stopwords 
    sw = stopwords.words('english')  
    l1 =[];l2 =[] 
      
    # remove stop words from the string 
    X_set = {w for w in X_list if not w in sw}  
    Y_set = {w for w in Y_list if not w in sw} 
      
    # form a set containing keywords of both strings  
    rvector = X_set.union(Y_set)  
    for w in rvector: 
        if w in X_set: l1.append(1) # create a vector 
        else: l1.append(0) 
        if w in Y_set: l2.append(1) 
        else: l2.append(0) 
    c = 0.0
    
    # cosine formula  
    for i in range(len(rvector)): 
            c+= l1[i]*l2[i]
    cosine = c / float((sum(l1)*sum(l2))**0.5) 

    # pdb.set_trace()
    return cosine


def intersecting_who(question, verbose=True):
    who_embeddings = embedder.encode(who_truths, convert_to_tensor=True)
    who_negs = [no_negation(truth) for truth in who_truths]
    who_negs = torch.from_numpy(np.asarray(who_negs))
    
    question_embedding = embedder.encode(question, convert_to_tensor=True)
    question_neg = no_negation(question)
    cos_scores = util.pytorch_cos_sim(question_embedding, who_embeddings)[0]
    cos_scores = cos_scores.cpu()*question_neg*who_negs
    cos_scores_nltk = [nltk_similarity(question, who_truths[ind])*question_neg*who_negs[ind]\
                for ind in range(len(who_truths))]

    if verbose:
        for ind in range(cos_scores.numpy().squeeze().shape[0]):
            print ('({},{}): \t\t{}'.format(cos_scores[ind], cos_scores_nltk[ind], who_truths[ind]))

    res = False
    mx_ind = np.argmax(cos_scores)
    if cos_scores[mx_ind] >= 0.8:
        if verbose:
            print (who_truths[mx_ind], question)
        res = True

    if res: 
        return (True, who_truths[mx_ind])
    else:
        return (False, -1) 

def get_scores(corpus, question, verbose=True):
    res, who_fact = intersecting_who(question, verbose=verbose)
    # pdb.set_trace()
    if res:
        print ('WHO FACT IS A MATCH')
        print (who_fact)
        return [[who_fact, 1.0]]

    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)
    corpus_negs = [no_negation(s) for s in corpus]
    corpus_negs = torch.from_numpy(np.asarray(corpus_negs))
    

    # Find the closest 5 sentences of the corpus for each question sentence based on cosine similarity
    top_k = 5

    question_embedding = embedder.encode(question, convert_to_tensor=True)
    question_neg = no_negation(question)
    cos_scores = util.pytorch_cos_sim(question_embedding, corpus_embeddings)[0]
    cos_scores = cos_scores.cpu()*question_neg*corpus_negs

    # temp = util.pytorch_cos_sim(embedder.encode('fact: drinking sanitiers does not prevent or cure corona virus'), embedder.encode('drinking sanitizers prevents corona virus'))
    # pdb.set_trace()
    #We use np.argpartition, to only partially sort the top_k results
    top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]

    if verbose:
        print("\n\n======================\n\n")
        print("question:", question)
        print("\nTop 5 most similar sentences in corpus:")

    res = []
    for idx in top_results[0:top_k]:
        cur_res = [corpus[idx].strip(), cos_scores[idx]]
        res.append(cur_res)
        if verbose:
            print(cur_res[0], "(Score: %.4f)" % (cur_res[1]))

    return res

def get_true_false(corpus, verbose=True):
    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)
    corpus_negs = [no_negation(s) for s in corpus]
    corpus_negs = torch.from_numpy(np.asarray(corpus_negs))

    
    query_embedding = embedder.encode('true', convert_to_tensor=True)
    query_neg = 1

    true_cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
    true_cos_scores = true_cos_scores.cpu()*corpus_negs
    
    
    query_embedding = embedder.encode('false', convert_to_tensor=True)
    query_neg = 1


    false_cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
    false_cos_scores = false_cos_scores.cpu()*corpus_negs
    res = []
    for i in range(len(corpus)):
        if true_cos_scores[i] > false_cos_scores[i]:
            res.append('True')
        else:
            res.append('False')

        if verbose:
            print(i,':',corpus[i],'\n\t',res[-1])
            print('true: ', true_cos_scores[i], 'false: ', false_cos_scores[i], '\n\n')

    return res


### spacy functions


nlp = spacy.load('en_core_web_sm')



def no_negation(query):

    doc = nlp('query')

    negation_tokens = [tok for tok in doc if tok.dep_ == 'neg']
    negation_head_tokens = [token.head for token in negation_tokens]
    if len(negation_tokens)>0:
        return -1
    else:
        return 1
    
    
    #for token in negation_head_tokens:
    #    print(token.text, token.dep_, token.head.text, token.head.pos_, \
    #                [child for child in token.children])


if __name__ == '__main__':
    no_negation(query)
