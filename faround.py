
coordinates = "127.00102191231232SEPERATOR-200.1283192831231231231"


def decompose_coordinates(coordinates):
	newcoordinates = coordinates.replace('SEPERATOR',',')
	index = 0
	for symbol in newcoordinates:
		index+=1
		if symbol == ",":
			latitude = newcoordinates[0:index-1]
			longitude = newcoordinates[index:len(newcoordinates)]
	return [latitude, longitude]




print(decompose_coordinates(coordinates))