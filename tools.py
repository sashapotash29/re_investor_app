import requests
import xmltodict
from datetime import datetime
import json
import time

EastTwentySecond = {'number': '121', 'street': '22nd', 'roadtype':'St', 'zip': '10010' }
FiftyOneParkPlace = {'number': '45', 'street': 'Park', 'roadtype':'Place', 'zip': '10007' }
SeventyFiveKenmare = {'number': '75', 'street': 'Kenmare', 'roadtype':'St', 'zip': '10012' }
ThreeThreeThreeSchermerhorn = {'number': '333', 'street': 'Schermerhorn', 'roadtype':'St', 'zip': '11217' }
FiveNineFiveBaltic = {'number': '595', 'street': 'Baltic', 'roadtype':'St', 'zip': '11217' }
FiveNineOneThirdAve = {'number': '591', 'street': '3rd', 'roadtype':'Ave', 'zip': '10016' }
TwoHundredGreene = {'number': '200', 'street': 'Greene', 'roadtype':'St', 'zip': '07302' }
TwoTwoFiveThirtyNine = {'number': '225', 'street': '39th', 'roadtype':'St', 'zip': '10016' }
FiveThreeOneMyrtle = {'number': '531', 'street': 'Myrtle', 'roadtype':'Ave', 'zip': '11205' }
FiveOneFiveThirtyEighth = {'number': '515', 'street': '38th', 'roadtype':'St', 'zip': '10018'}
SixtyWhite = {'number': '60', 'street': 'White', 'roadtype':'St', 'zip': '10013' }
FourZeroThreeGreenwich = {'number': '403', 'street': 'Greenwich', 'roadtype':'St', 'zip': '10013'}
OneSixOneColumbia = {'number': '161', 'street': 'Columbia', 'roadtype':'St', 'zip': '11231' }
FourFiveZeroUnion = {'number': '450', 'street': 'Union', 'roadtype':'St', 'zip': '11231' }
ThreeZeroEightThirtyEighth = {'number': '308', 'street': '38th', 'roadtype':'St', 'zip': '10016' }

prop_list = [EastTwentySecond,FiftyOneParkPlace,SeventyFiveKenmare,ThreeThreeThreeSchermerhorn,FiveNineFiveBaltic,FiveNineOneThirdAve,TwoHundredGreene, TwoTwoFiveThirtyNine, FiveThreeOneMyrtle, FiveOneFiveThirtyEighth, SixtyWhite, FourZeroThreeGreenwich, OneSixOneColumbia,FourFiveZeroUnion,ThreeZeroEightThirtyEighth]
for obj in prop_list:
	zillow_url = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=X1-ZWz19b6m5nu617_3jtqm&address='+obj['number']+'+'+obj['street']+'+'+obj['roadtype']+'&citystatezip='+obj['zip']
	results = requests.get(zillow_url).content
	okay = results.decode(encoding='UTF-8')
	okay = xmltodict.parse(okay)['SearchResults:searchresults']['response']['results']['result']
	zpid_list = []
	if len(okay )== 5:
		z = okay
		print(z)
		if type(z) == list:
			for item in z:
				for key, value in item.items():
					if key == 'zpid':
						zpid_list.append(value)
						print("ONLY ONE zpid has been added")
						print("END")
		else:
			for key, value in z.items():
				if key =='zpid':
					zpid_list.append(value)
					print("ONLY ONE zpid has been added")
					print("END")
	else:
		for index in range(0, len(okay)):
			z = okay[index]
			for key, value in z.items():
				if key =='zpid':
					zpid_list.append(value)
					print("zpid has been added")
			print("END")

	print(zpid_list)
	for zpid in zpid_list:
		zpid_url = 'http://www.zillow.com/webservice/GetDeepComps.htm?zws-id=X1-ZWz19b6m5nu617_3jtqm&zpid='+zpid+'&count=5'
		result = requests.get(zpid_url).content.decode(encoding='UTF-8')
		# CHECK IF THE DEEP COMPS RETURNED A INFROMATION
		dict_result = xmltodict.parse(result)
		print(dict_result['Comps:comps']['message']['text'])
		if 'Error' not in dict_result['Comps:comps']['message']['text']:
			dict_form = xmltodict.parse(result)['Comps:comps']['response']
			for key, value in dict_form['properties'].items():
				if key =="principal":
					prop_obj_list = []
					principal_dict = value
					print(principal_dict)
					key_list = []
					for key, value in principal_dict.items():
						key_list.append(key)
					print(key_list)
					address_info = principal_dict['address']
					print('address')
					print(address_info)
					address = address_info['street']
					print(address)
					city = address_info['city']
					zipcode = address_info['zipcode']
					print(zipcode)
					state = address_info['state']
					print(state)
					if 'finishedSqFt' in key_list:
						sq_ft = principal_dict['finishedSqFt']
					else:
						sq_ft = '0'
					if 'bedrooms' in key_list:
						bedrooms = principal_dict['bedrooms']
					else:
						bedrooms = '0'
					print('Bathrooms: ' + bedrooms)
					if 'bedrooms' in key_list:
						bathrooms = principal_dict['bathrooms']
					else:
						bathrooms = '0'
					print('Bathrooms: '  + bathrooms)
					zestimate_dict = principal_dict['zestimate']
					price = zestimate_dict['amount']['#text']
					date = datetime.strptime(zestimate_dict['last-updated'],'%m/%d/%Y').date()
					coordinates = address_info['latitude'] + "SEPERATOR" + address_info['longitude']
					print(date)
					print('zestimate_dict')
					print(zestimate_dict)
					print(price)
					request_obj = {
						'building_name': "no_name",
						'date_updated': str(date),
						'coordinates': coordinates,
						'sq_ft': sq_ft,
						'bedrooms': bedrooms,
						'bathrooms': bathrooms,
						'address': address,
						'city': city,
						'state': state,
						'zipcode': zipcode,
						'current_price': price

					}
					prop_obj_list.append(request_obj)
					final_product = {}
					final_product['result'] = prop_obj_list
					print('')
					print("REQUEST TIME")
					print('')

					r = requests.post('http://127.0.0.1:8000/onlyforprops',data=json.dumps(final_product))
					print('')
					print("REQUEST PROCESSED")
					print('')

					print(r.status_code, r.reason,'property finished')

		# final_product = {}
		# final_product['result'] = prop_obj_list

		else:
			print('')
			print("No Information found in the deep comps")
			print('')




