import requests
import pdb

api_url = 'https://factchecktools.googleapis.com/v1alpha1/claims:search'
query = {'query': 'coronavirus is a type of rabies', 'key': 'AIzaSyCtfHm7PXk1ZD_vcXihKzUk5rNO287S0DY'}
response = requests.get(api_url, params=query, headers={'Content-Type':'application/json'})
if response.status_code != 200:
    # This means something went wrong.
    print ('DID NOT WORK!')
else:
	resp_json = response.json()
	for claim in resp_json['claims']:
		for review in claim['claimReview']:
			print (review['textualRating'])
    	# print('{} {}'.format(todo_item['id'], todo_item['summary']))

'''
GET https://factchecktools.googleapis.com/v1alpha1/claims:search?query=is%20google%20real&key=AIzaSyCtfHm7PXk1ZD_vcXihKzUk5rNO287S0DY HTTP/1.1

Accept: application/json


curl \
  'https://factchecktools.googleapis.com/v1alpha1/claims:search?query=is%20google%20real&key=955767f0032cf20f122a012549e42d11eb4f398c' \
  --header 'Accept: application/json' \
  --compressed

{'text': 'Novel coronavirus is a virus, not a bacterium easily treated with aspirin', 
'claimant': 'Facebook',
'claimDate': '2020-05-28T00:00:00Z',
'claimReview': 
[{'publisher': {'name': 'USA Today', 'site': 'usatoday.com'}, 'url': 'https://www.usatoday.com/story/news/factcheck/2020/05/29/fact-check-covid-19-caused-virus-not-bacteria/5277398002/', 'title': 'Fact check: COVID-19 is caused by a virus, not by bacteria', 'reviewDate': '2020-05-29T00:00:00Z', 'textualRating': 'False', 'languageCode': 'en'}]}
'''