import requests
import json
import sys

from nwsURLS import NWSURLS


# To obtain mapQuest API key, create free account at developer.mapquest.com
# mapQuest API required for geocoding (turning city name to latitide and longitude)
# National Weather Service does not require an account to use API.


mapQuestApiKey = '5S4GY9hSFme8nx7MFofVZojJCPAPeVEb'

def save_url(key):
	with open('nwsURLS.py', 'a') as f:
		f.write('NWSURLS[\'%s\'] = \'%s\'\n' % (key, NWSURLS[key]))

def jprint(obj):
	text = json.dumps(obj, sort_keys=True, indent=4)
	print(text)

def call_api(apiURL):
	response = requests.get(apiURL)
		

	if response.status_code == 200:
		# responseDict = json.loads(jsonResponse)
		return response.json()

	else:
		print('Error with API %s' % apiURL)
		print('Error %i' % response.status_code)
		print()
		# print(json.dumps(responseDict, sort_keys=True, indent=4))

		sys.exit()


def get_forecast(city, state):
	key = city.lower() + state.lower()

	try:
		apiURL = NWSURLS[key]

	except KeyError:
		NWSURLS[key] = get_city_nws_url(city, state)

		save_url(key)

		apiURL = NWSURLS[key]


	forecast = call_api(apiURL)

	return forecast


def get_city_nws_url(city, state):

	geocode = get_geocode(city, state) # lattitude and longitude of city according to MapQuest API

	# Get NWS office and grid coordinates for specified city

	apiURL = 'https://api.weather.gov/points/%s,%s' % geocode

	nwsReturn = call_api(apiURL)

	cityUrl = nwsReturn['properties']['forecast']

	return cityUrl

def get_geocode(city, state):

	parameters = (mapQuestApiKey, city, state)

	apiURL  = 'http://open.mapquestapi.com/geocoding/v1/address?key=%s&location=%s,%s&outformat=json' % parameters

	mapQuestReturn = call_api(apiURL)

	lat = mapQuestReturn['results'][0]['locations'][0]['latLng']['lat']
	lon = mapQuestReturn['results'][0]['locations'][0]['latLng']['lng']

	return (lat, lon)


def input_location():
	print('Get weather for where?')
	city = input('City: ').rstrip()
	state = input('State: ').rstrip()

	return city, state


def main():


	if len(sys.argv) == 1:
		city, state = input_location()

	elif len(sys.argv) == 2:
		city, state = sys.argv[1].split(',')

	elif len(sys.argv) >= 3:
		city = ' '.join(sys.argv[1:-1])
		state = sys.argv[-1]


	# print('%s, %s' % (city, state))

	forecast = get_forecast(city, state)

	# # jprint(forecast)
	print()
	print(forecast['properties']['periods'][0]['detailedForecast'])
	print()


if __name__ == '__main__':
	main()