from sentence_transformers import SentenceTransformer, util
import numpy as np

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
# 'According to current evidence,corona virus is primarily transmitted between people through respiratory droplets and contact routes.2-7 In an ',
# 'How is the virus that causes corona virus most commonly transmitted between people? Current evidence suggests that corona virus spreads ',
# 'Current evidence suggests that SARS-CoV-2, the virus that causes corona virus is predominantly spread from person-to-person. Understanding ',
# 'How are corona virus and influenza viruses similar? The serial interval for corona virus is estimated to be 5-6 days, while for influenza virus, ',
# 'Current understanding of transmission risk. Infection with the virus causing corona virus SARS-CoV-2) is confirmed by the presence of viral RNA ',
# 'Droplets spread virus. By following good respiratory hygiene, you protect the people around you from viruses such as cold, flu andcorona virus', 
# 'corona virus is a hoax', 
# 'tarana wants to sleep']
# queries ['coronavirus is a virus']

# corpus = [
# 'FACT: Vaccines against pneumonia doesn\'t protect against the corona virus',
# 'FACT: Vaccines against pneumonia protects against the corona virus',
# 'WHO continues to recommend neonatal BCG vaccination in countries or WHO does not recommend BCG vaccination for the prevention of corona. BCG Vaccination to Protect Healthcare Workers Against corona ',
# 'Fact sheet from WHO on immunization coverage: provides key facts and information (DTP3) vaccine, protecting them against infectious diseases that can cause. Haemophilus influenzae type b (Hib) causes meningitis and pneumonia. the use of vaccines to protect people of all ages against disease',
# 'As the world waits for a vaccine to defeat the corona pandemic, we. This level of protection comes through a strong global effort to increase vaccine and pneumonia, diarrhoea, and the worlds first-ever malaria vaccine so that when we have a safe and effective vaccine, no one will be left behind',
# 'Many vaccines can also protect when administered after exposure – examples. In field trials, mortality and morbidity reductions were seen for pneumococcal ',
# 'Vaccines reduce risks of getting a disease by working with your body natural defences to build protection. When you get a vaccine, your immune system ',
# 'disease corona and on next steps in readiness and with pneumonia of unknown etiology – a surveillance definition established following the. However, they do not appear to be major drivers of the overall measures to slow transmission of the corona virus, reduce disease and save lives',
# 'Most people infected with the corona virus will experience mild to moderate. Protect yourself and others from infection by washing your hands or using an alcohol At this time, there are no specific vaccines or treatments for corona', 
# 'Despite their success in preventing disease, vaccines rarely protect 100 of the recipients. Administration of other vaccines will be advised on the basis of a travel risk. Important cause of pneumonia, meningitis, septicaemia, epiglottitis and',
# 'Myth 2: The flu vaccine can give me the flu. Fact: The However, being vaccinated improves the chance of being protected from the flu. This is especially'
# ]
# queries = ['there is no vaccine for coronavirus']

# corpus = [
# 'Rabies is a zoonotic disease (a disease that is transmitted from animals to humans, Furious rabies is the most common form of human rabies, accounting for ',
# 'Rabies infection manifests in two forms of rabies: furious (classical or encephalitic) form and the paralytic form. Furious rabies accounts for approximately 80 of',
# 'Paralytic rabies accounts for about 20 of the total number of human cases. This form of rabies runs a less dramatic and usually longer course',
# 'Rabies is a viral zoonotic disease that causes progressive and fatal inflammation of the brain and spinal cord',
# 'Rabies is estimated to cause 59 000 human deaths annually in over 150 countries, with 95 of cases occurring in Africa and Asia. Due to widespread ',
# 'Children are at particular risk. Two types of vaccines to protect against rabies in humans exist - nerve tissue and cell culture vaccines. WHO recommends ',
# 'Recommendations for post-exposure depend on the type of contact with the suspected rabid animal. For category I exposure (touching or ',
# 'Rabies is a significant health concern following dog bites, cat bites and The health impacts of animal bites are dependent on the type and ',
# 'Human rabies is a 100% vaccine-preventable disease, yet it continues to kill. Rabies vaccinations are highly effective, safe and well tolerated. The WHO ',
# 'Over the past few years, many countries have acted to strengthen rabies control efforts—scaling up dog vaccination programmes, making human'
# ]
# queries = ['would pneumonia vaccine protect me from corona virus']

# corpus = [
# 'Highlighting some of the misinformation circulating on COVID-19. Bleach and disinfectant should be used carefully to disinfect surfaces only. Drinking methanol, ethanol or bleach DOES NOT prevent or cure COVID-19 and can be ', 
# 'Keep alcohol-based hand sanitizers out of childrens reach. Apply a coin-sized amount on your hands. Avoid touching your eyes, mouth and '
# 'Regularly wash hands with soap and water or alcohol-based hand sanitizer Fact: There is no scientific evidence that lemon/turmeric prevents COVID-19',
# 'Todays handrubs all contain skin softeners which help prevent drying. Of the published studies available, many describe that nurses who routinely use alcohol',
# 'for preventing and for protecting human health during all infectious disease outbreaks, including of coronavirus disease 2019 (COVID-19)',
# 'Consequently, hand hygiene is extremely important to prevent the spread of the COVID-19 virus. It also interrupts transmission of other viruses and bacteria ',
# 'Q&A: Considerations for the cleaning and disinfection of environmental surfaces in the context of COVID-19 in non-health care settings ',
# 'How can you clean soiled bedding, towels and linens from patients with COVID-19?',
# 'Simple ways to prevent the spread of COVID-19 in your workplace. 2. How to Put sanitizing hand rub dispensers in prominent places around the workplace. Encourage regular hand-washing or use of an alcohol rub by all ',
# 'Alternative drinking-water disinfectants: bromine, iodine and silver. used; these are generally used to prevent the silver nanoparticles from aggregating or '
# ]
# query = 'drinking sanitizers prevent corona virus'

# corpus = [
# 'People should NOT wear masks when exercising, as masks may reduce the ability The important preventive measure during exercise is to maintain physical',
# 'Should children with developmental disabilities wear masks? Should children wear a mask when playing sports or doing physical activities?',
# 'other equally relevant measures should be adopted. If masks are to be Wearing medical masks when not indicated may cause unnecessary',
# 'Why do we need it? Regular So how do I stay safe while exercising in COVID-19? Do not How do I stay active in and around the home?',
# 'Advice on the use of masks in the context of COVID-19. Interim guidance. Infection prevention and control / WASH. AddThis Sharing',
# 'Does WHO recommend routine wearing masks for healthy people during the 2019 nCoV outbreak?',
# 'Masks on their own will not protect you from COVID-19. person at home should wear a medical mask while they are in the same room as the ',
# 'Media Statement: the role and need of masks during COVID-19 outbreak. “If you do not wear the mask properly, touch the mask with unwashed hands, Before putting on a mask, clean hands with soap and running water or ',
# 'COVID-19 transmission & disease severity in young people. Guidance on 5 years and younger should not be required to wear masks. Questions about how to stay safe while exercising and how to stay active at ',
# 'But how do you do this in Senegal, where there are more than a dozen languages? In a bid to A woman exercises while wearing a face mask in Dakar, Sengal. ... In this new COVID era, however, it is not so much a time for concerts as it is for'
# ]
# queries = ['i should not wear masks while exercising']

def get_scores(corpus, query):
  corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

  # Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
  top_k = 5

  query_embedding = embedder.encode(query, convert_to_tensor=True)
  cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
  cos_scores = cos_scores.cpu()

  #We use np.argpartition, to only partially sort the top_k results
  top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]

  print("\n\n======================\n\n")
  print("Query:", query)
  print("\nTop 5 most similar sentences in corpus:")

  for idx in top_results[0:top_k]:
      print(corpus[idx].strip(), "(Score: %.4f)" % (cos_scores[idx]))

if __name__ == 'main':
  get_scores(corpus, query)