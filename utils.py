import spacy
from spacy import displacy

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
