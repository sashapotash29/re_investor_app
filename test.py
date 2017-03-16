import requests
import beautifulsoup4

# PLAN
# 1. URL FOR PROPERTIES IN NYC
# - ENSURE AVAILABLE
# - MORTGAGES FOR SIMILAR PLACES


property_url = ''


prop_results = requests.get(property_url).content


property_soup = BeautifulSoup(prop_results)

print(property_soup)

for prop in property_soup('items'):
	print(prop.string)




