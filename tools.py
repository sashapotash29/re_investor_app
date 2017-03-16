import requests
import xmltodict



prop_url = 'https://api.simplyrets.com/properties?cities=Houston'
zillow_url = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=X1-ZWz19b6m5nu617_3jtqm&address=625+57th+St&citystatezip=10019'
results = requests.get(zillow_url).content

okay = results.decode(encoding='UTF-8')

okay = xmltodict.parse(okay)['SearchResults:searchresults']['response']['results']['result']

# print(okay)
zpid_list = []
for index in range(0, len(okay)):
	print("START")
	z = okay[index]
	for key, value in z.items():
		print("======================")
		print(key)
		print(value)
		print("======================")
		if key =='zpid':
			zpid_list.append(value)
			print("zpid has been added")
	print("END")

print(zpid_list)

for zpid in zpid_list:
	zpid_url = 'http://www.zillow.com/webservice/GetDeepComps.htm?zws-id=X1-ZWz19b6m5nu617_3jtqm&zpid='+zpid
	result = requests.get(zpid_url).content.decode(encoding='UTF-8')
	dict_form = xmltodict.parse(result)
	print (dict_form)





