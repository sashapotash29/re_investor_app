import requests
import xmltodict
from datetime import datetime
import json
# from app import db
# from models import Property

EastTwentySecond = {'number': '121', 'street': '22nd', 'roadtype':'St', 'zip': '10010' }
FiftyOneParkPlace = {'number': '45', 'street': 'Park', 'roadtype':'Place', 'zip': '10007' }
SeventyFiveKenmare = {'number': '75', 'street': 'Kenmare', 'roadtype':'St', 'zip': '10012' }
ThreeThreeThreeSchermerhorn = {'number': '333', 'street': 'Schermerhorn', 'roadtype':'St', 'zip': '11217' }
FiveNineFiveBaltic = {'number': '595', 'street': 'Baltic', 'roadtype':'St', 'zip': '11217' }


prop_url = 'https://api.simplyrets.com/properties?cities=Houston'
zillow_url = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=X1-ZWz19b6m5nu617_3jtqm&address=591+3rd+Ave&citystatezip=10016'
zillow_url = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=X1-ZWz19b6m5nu617_3jtqm&address=333+Schermerhorn+St&citystatezip=11217'
results = requests.get(zillow_url).content

okay = results.decode(encoding='UTF-8')
print(okay)
okay = xmltodict.parse(okay)['SearchResults:searchresults']['response']['results']
print(okay)
print(len(okay))
zpid_list = []
for index in range(0, len(okay)):
	if len(okay)== 5:
		z = okay
		for key, value in z.items():
		if key =='zpid':
			zpid_list.append(value)
			print("zpid has been added")
	print("END")
	else:
	for key, value in z.items():
		# print("======================")
		# print(key)
		# print(value)
		# print("======================")
		if key =='zpid':
			zpid_list.append(value)
			print("zpid has been added")
	print("END")

print(zpid_list)

# prop_obj_list = []
# for zpid in zpid_list:
# 	zpid_url = 'http://www.zillow.com/webservice/GetDeepComps.htm?zws-id=X1-ZWz19b6m5nu617_3jtqm&zpid='+zpid+'&count=5'
# 	result = requests.get(zpid_url).content.decode(encoding='UTF-8')
# 	print(result)
# 	# CHECK IF THE DEEP COMPS RETURNED A INFROMATION
# 	dict_result = xmltodict.parse(result)
# 	print(dict_result['Comps:comps']['message']['text'])
# 	if 'Error' not in dict_result['Comps:comps']['message']['text']:
# 		dict_form = xmltodict.parse(result)['Comps:comps']['response']
# 		for key, value in dict_form['properties'].items():
# 			if key =="principal":
# 				principal_dict = value
# 				print(principal_dict)
# 				key_list = []
# 				for key, value in principal_dict.items():
# 					key_list.append(key)
# 				print(key_list)
# 				address_info = principal_dict['address']
# 				print('address')
# 				print(address_info)
# 				address = address_info['street']
# 				print(address)
# 				city = address_info['city']
# 				zipcode = address_info['zipcode']
# 				print(zipcode)
# 				state = address_info['state']
# 				print(state)
# 				if 'finishedSqFt' in key_list:
# 					sq_ft = principal_dict['finishedSqFt']
# 				else:
# 					sq_ft = '0'
# 				bedrooms = principal_dict['bedrooms']
# 				print(bedrooms)
# 				bathrooms = principal_dict['bathrooms']
# 				print(bathrooms)
# 				zestimate_dict = principal_dict['zestimate']
# 				price = zestimate_dict['amount']['#text']
# 				date = datetime.strptime(zestimate_dict['last-updated'],'%m/%d/%Y').date()
# 				coordinates = address_info['latitude'] + "SEPERATOR" + address_info['longitude']
# 				print(date)
# 				print('zestimate_dict')
# 				print(zestimate_dict)
# 				print(price)
# 				request_obj = {
# 					'building_name': "no_name",
# 					'date_updated': str(date),
# 					'coordinates': coordinates,
# 					'sq_ft': sq_ft,
# 					'bedrooms': bedrooms,
# 					'bathrooms': bathrooms,
# 					'address': address,
# 					'city': city,
# 					'state': state,
# 					'zipcode': zipcode,
# 					'current_price': price

# 				}
# 				prop_obj_list.append(request_obj)

# 				final_product = {}
# 				final_product['result'] = prop_obj_list

# 		r = requests.post('http://127.0.0.1:5000/onlyforprops',data=json.dumps(final_product))
# 		print(r.status_code, r.reason,'property finished')

# 	else:
# 		print('')
# 		print("No Information found in the deep comps")
# 		print('')
# 		pass
		


# 		# # SCHEMA
# 		# id = db.Column(db.Integer, primary_key=True)
# 		# building_name = db.Column(db.String(40), primary_key=True)
# 		# date_updated = db.Column(db.Date)
# 		# sq_ft = db.Column(db.Float, primary_key=True)
# 		# bedrooms = db.Column(db.Float, primary_key=True)
# 		# bathrooms = db.Column(db.Float, primary_key=True)
# 		# address = db.Column(db.String(100))
# 		# city = db.Column(db.String(30))
# 		# state = db.Column(db.String(20))
# 		# zipcode = db.Column(db.String(30))
# 		# past_price = db.Column(db.Float)
# 		# current_price = db.Column(db.Float)
# 		# status = db.Column(db.String)




